from fastapi import HTTPException, UploadFile

from app.repositories import UserRepository, FileRepository
from app.schemas import FileCreate, FileScheme, StreamingFile
from app.core import minio

from .base import BaseService, with_unit_of_work


__all__ = ["StorageService"]


class StorageService(BaseService):
    @with_unit_of_work
    async def upload_file(self, user_id: int, file: UploadFile) -> FileScheme:
        if not await self.uow.get_repository(UserRepository).exists_user_with_id(user_id):
            raise HTTPException(status_code=401, detail="Only authorized users can upload files")
        try:
            obj = minio.upload_file(file)
        except ValueError as e:
            raise HTTPException(409, f"Failed to upload file: {str(e)}")
        return await self.uow.get_repository(FileRepository).create_one(
            FileCreate(owner_id=user_id, filename=obj.object_name).model_dump(),
            FileScheme
        ) # TODO: Надо удостоверяться, что добавление в minio и БД происходит по ACID
    
    @with_unit_of_work
    async def get_file_meta(self, file_id: int, user_id: int | None) -> FileScheme:
        file = await self.uow.get_repository(FileRepository).get_by_id(file_id, FileScheme)
        if file is None:
            raise HTTPException(status_code=404, detail="File not found")
        if not file.is_public and file.owner_id != user_id:
            raise HTTPException(status_code=403, detail="File is private")
        return file
    
    @with_unit_of_work
    async def get_file(self, file_id: int, user_id: int | None) -> StreamingFile:
        file_meta = await self.get_file_meta(file_id, user_id)
        return StreamingFile(
            metadata=file_meta, 
            stream=minio.get_file_stream(file_meta.filename)
        )
    
    @with_unit_of_work
    async def delete_file(self, file_id: int, user_id: int):
        if not await self.uow.get_repository(UserRepository).exists_user_with_id(user_id):
            raise HTTPException(status_code=401, detail="Only authorized owners can delete files")
        file_meta = await self.get_file_meta(file_id, user_id)
        if file_meta.owner_id != user_id:
            raise HTTPException(status_code=401, detail="Only authorized owners can delete files")
        try:
            minio.delete_file(file_meta.filename)
        except ValueError as e:
            raise HTTPException(404, f"Failed to delete file: {str(e)}")
        await self.uow.get_repository(FileRepository).delete_by_id(file_id) # TODO: Надо удостоверяться, что удаление из minio и БД происходит по ACID
        
