from fastapi import APIRouter, UploadFile
from fastapi.responses import StreamingResponse, Response
from urllib.parse import quote

from app.schemas import FileMeta

from .dependencies import UserIdDep, UserIdSoftDep, StorageServiceDep


router = APIRouter(
    prefix='/storage',
    tags=['storage']
)


@router.post('/', response_model=FileMeta)
async def add_file(
    user_id: UserIdDep, storage_service: StorageServiceDep, 
    file: UploadFile
) -> FileMeta:
    return await storage_service.upload_file(user_id, file)


@router.get('/{file_id}/meta', response_model=FileMeta)
async def get_file_meta(
    file_id: int, user_id: UserIdSoftDep, 
    storage_service: StorageServiceDep
) -> FileMeta:
    return await storage_service.get_file_meta(file_id, user_id)


@router.get('/{file_id}/cards', response_model=list[int])
async def get_file_cards(
    file_id: int, user_id: UserIdDep, 
    storage_service: StorageServiceDep
) -> list[int]:
    return await storage_service.get_file_cards(file_id, user_id)


@router.get('/{file_id}', response_class=StreamingResponse)
async def get_file(
    file_id: int, user_id: UserIdSoftDep, 
    storage_service: StorageServiceDep
) -> StreamingResponse:
    file = await storage_service.get_file(file_id, user_id)
    return StreamingResponse(
        file.stream,
        media_type="application/octet-stream",
        headers={
            "Content-Disposition": f"attachment; filename={quote(file.metadata.filename)}",
            'Content-Type': f'{file.metadata.type}/{file.metadata.ext}'
        }
    )


@router.delete('/{file_id}', response_class=Response)
async def delete_file(
    file_id: int, user_id: UserIdDep, 
    storage_service: StorageServiceDep
):
    await storage_service.delete_file(file_id, user_id)