from fastapi import APIRouter, HTTPException, UploadFile
from fastapi.responses import StreamingResponse
from urllib.parse import quote

from app.schemas.storage import FileUploadedScheme
from app.crud.storage import (
    get_file_stream, 
    get_files_list, 
    is_file_exists, 
    upload_file,
    delete_file
)


router = APIRouter(
    prefix='/storage',
    tags=['storage']
)


@router.get('/{user_id}/{filename}', response_class=StreamingResponse)
def get_file(user_id: int, filename: str):
    try:
        return StreamingResponse(
            get_file_stream(f'{user_id}/{filename}'),
            media_type="application/octet-stream",
            headers={"Content-Disposition": f"attachment; filename={filename}"}
        )
    except:
        raise HTTPException(404, 'File not found')
    

@router.get('/{user_id}', response_model=list[FileUploadedScheme])
def list_files(user_id: int):
    return [
        FileUploadedScheme(url=f'/storage/{quote(obj.object_name)}') 
        for obj in get_files_list(user_id)
    ]


@router.post('/{user_id}', response_model=FileUploadedScheme)
def add_file(user_id: int, file: UploadFile):
    # TODO: User is owner checking
    full_path = f'{user_id}/{file.filename}'
    if is_file_exists(full_path):
        raise HTTPException(409, 'File with this name already exists')
    try:
        upload_file(full_path, file.file, file.size)
        return FileUploadedScheme(
            url=router.url_path_for(
                'get_file', user_id=user_id, filename=quote(file.filename)
            )
        )
    except ValueError as e:
        raise HTTPException(409, 'Failed to upload file: ' + e.message)


@router.delete('/{user_id}/{filename}')
def delete_file(user_id: int, filename: str):
    # TODO: User is owner checking
    full_path = f'{user_id}/{filename}'
    if not is_file_exists(full_path):
        raise HTTPException(409, 'File doesn\'t exist')
    try:
        delete_file(full_path)
        return {}
    except ValueError as e:
        raise HTTPException(404, 'Failed to delete file: ' + e.message)
