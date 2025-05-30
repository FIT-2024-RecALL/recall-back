from fastapi import HTTPException, UploadFile

from app.repositories import UserRepository, FileRepository, FileCardRepository
from app.schemas import FileCreate, get_allowed_types, get_allowed_exts, FileMeta, StreamingFile
from app.core import minio, get_settings

from .base import BaseService, with_unit_of_work


__all__ = ["StorageService"]

class StorageService(BaseService):
    @with_unit_of_work
    async def upload_file(self, user_id: int, file: UploadFile) -> FileMeta:
        if file.size > get_settings().max_file_bytes_size:
            raise HTTPException(status_code=413, detail=f"Max file's size is {get_settings().max_file_mb_size} MB")
        if not await self.uow.get_repository(UserRepository).exists_user_with_id(user_id):
            raise HTTPException(status_code=401, detail="Only authorized users can upload files")
        file_type, file_ext = file.content_type.split("/")
        if file_type is None or file_ext is None or file_type not in get_allowed_types() or file_ext not in get_allowed_exts():
            raise HTTPException(status_code=409, detail="Invalid file type")
        try:
            obj = await minio.upload_file(file)
        except ValueError as e:
            raise HTTPException(409, f"Failed to upload file: {str(e)}")
        return await self.uow.get_repository(FileRepository).create_one(
            FileCreate(
                owner_id=user_id,
                type=file_type,
                ext=file_ext,
                filename=obj.object_name,
                size=file.size
            ).model_dump(),
            FileMeta
        )
    
    @with_unit_of_work
    async def get_file_meta(self, file_id: int, user_id: int | None) -> FileMeta:
        file = await self.uow.get_repository(FileRepository).get_by_id(file_id, FileMeta)
        if file is None:
            raise HTTPException(status_code=404, detail="File not found")
        if not file.is_public and file.owner_id != user_id:
            raise HTTPException(status_code=403, detail="File is private")
        return file
    
    @with_unit_of_work
    async def get_file_cards(self, file_id: int, user_id: int) -> list[int]:
        file_meta = await self.get_file_meta(file_id, user_id)
        if file_meta.owner_id != user_id:
            raise HTTPException(status_code=401, detail="Only authorized owners can get file's cards")
        return await self.uow.get_repository(FileCardRepository).get_file_cards_ids(file_id)
    
    @with_unit_of_work
    async def get_file(self, file_id: int, user_id: int | None) -> StreamingFile:
        file_meta = await self.get_file_meta(file_id, user_id)
        stream = await minio.get_file_stream(file_meta.filename)
        if not stream:
            raise HTTPException(status_code=400, detail="Failed to get file")
        return StreamingFile(metadata=file_meta, stream=stream)
    
    @with_unit_of_work
    async def delete_file(self, file_id: int, user_id: int):
        if not await self.uow.get_repository(UserRepository).exists_user_with_id(user_id):
            raise HTTPException(status_code=401, detail="Only authorized owners can delete files")
        file_meta = await self.get_file_meta(file_id, user_id)
        if file_meta.owner_id != user_id:
            raise HTTPException(status_code=401, detail="Only authorized owners can delete files")
        try:
            await minio.delete_file(file_meta.filename)
        except ValueError as e:
            raise HTTPException(404, f"Failed to delete file: {str(e)}")
        await self.uow.get_repository(FileRepository).delete_by_id(file_id)
