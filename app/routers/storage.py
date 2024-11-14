from fastapi import APIRouter, HTTPException, UploadFile, File
from fastapi.responses import StreamingResponse, Response
from urllib.parse import quote

from app.schemas.storage import FileUploadedScheme
import app.crud as crud


router = APIRouter(
    prefix='/storage',
    tags=['storage']
)


@router.get('/{user_id}/{filename}', response_class=StreamingResponse)
def get_file(user_id: int, filename: str):
    try:
        return StreamingResponse(
            crud.storage.get_file_stream(f'{user_id}/{filename}'),
            media_type="application/octet-stream",
            headers={"Content-Disposition": f"attachment; filename={filename}"}
        )
    except:
        raise HTTPException(404, 'File not found')
    

@router.get('/{user_id}', response_model=list[FileUploadedScheme])
def list_files(user_id: int):
    return [
        FileUploadedScheme(url=f'/storage/{quote(obj.object_name)}')
        for obj in crud.storage.get_files_list(user_id)
    ]


@router.post('/{user_id}', response_model=FileUploadedScheme)
def add_file(user_id: int, file: UploadFile = File(...)):
    # TODO: User is owner checking
    try:
        obj = crud.storage.upload_file(user_id, file)
        return FileUploadedScheme(
            url=f'/storage/{quote(obj.object_name)}'
        )
    except ValueError as e:
        raise HTTPException(409, f'Failed to upload file: {e.message}')


@router.delete('/{user_id}/{filename}', status_code=200)
def delete_file(user_id: int, filename: str):
    # TODO: User is owner checking
    full_path = f'{user_id}/{filename}'
    if not crud.storage.is_file_exists(full_path):
        raise HTTPException(404, 'File not found')
    try:
        crud.storage.delete_file(full_path)
        return Response(status_code=200)
    except ValueError as e:
        raise HTTPException(404, f'Failed to delete file: {e.message}')
