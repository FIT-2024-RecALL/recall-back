from fastapi import APIRouter, HTTPException, UploadFile, File
from fastapi.responses import StreamingResponse, Response
from urllib.parse import quote

from app.schemas import FileUploadedScheme
from app.repositories import storage, UserRepository

from .dependencies import UserIdDep, UnitOfWorkDep


router = APIRouter(
    prefix='/storage',
    tags=['storage']
)


@router.get('/{user_id}/{filename}', response_class=StreamingResponse)
def get_file(user_id: int, filename: str):
    full_path = f'{user_id}/{filename}'
    if not storage.is_file_exists(full_path):
        raise HTTPException(404, "File not found")
    try:
        return StreamingResponse(
            storage.get_file_stream(full_path),
            media_type="application/octet-stream",
            headers={"Content-Disposition": f"attachment; filename={quote(filename)}"}
        )
    except ValueError as e:
        raise HTTPException(404, f"File not found: {str(e)}")


@router.get('/', response_model=list[FileUploadedScheme])
async def list_files(user_id: UserIdDep, uow: UnitOfWorkDep):
    if not await uow.get_repository(UserRepository).exists_user_with_id(user_id):
        raise HTTPException(status_code=400)  ## ТУТ ДОЛЖНО БЫТЬ КАСТОМНОЕ ИСКЛЮЧЕНИЕ!
    return [
        FileUploadedScheme(url=f"/storage/{quote(obj.object_name)}", filename=obj.object_name.split('/')[1])
        for obj in storage.get_files_list(user_id)
    ]


@router.post('/', response_model=FileUploadedScheme)
async def add_file(user_id: UserIdDep, uow: UnitOfWorkDep, file: UploadFile = File(...)):
    if not await uow.get_repository(UserRepository).exists_user_with_id(user_id):
        raise HTTPException(status_code=400)  ## ТУТ ДОЛЖНО БЫТЬ КАСТОМНОЕ ИСКЛЮЧЕНИЕ!
    try:
        obj = storage.upload_file(user_id, file)
        return FileUploadedScheme(
            url=f"/storage/{quote(obj.object_name)}",
            filename=obj.object_name.split('/')[1]
        )
    except ValueError as e:
        raise HTTPException(409, f"Failed to upload file: {str(e)}")


@router.delete('/{filename}', status_code=200)
async def delete_file(user_id: UserIdDep, filename: str, uow: UnitOfWorkDep):
    if not await uow.get_repository(UserRepository).exists_user_with_id(user_id):
        raise HTTPException(status_code=400)  ## ТУТ ДОЛЖНО БЫТЬ КАСТОМНОЕ ИСКЛЮЧЕНИЕ!
    full_path = f'{user_id}/{filename}'
    if not storage.is_file_exists(full_path):
        raise HTTPException(404, "File not found")
    try:
        storage.delete_file(full_path)
        return Response(status_code=200)
    except ValueError as e:
        raise HTTPException(404, f"Failed to delete file: {str(e)}")
