from fastapi import APIRouter, HTTPException, UploadFile
from fastapi.responses import FileResponse

import os

from app.storage import storage, bucket_name
from app.schemas.storage import FileUploadedScheme
from minio import S3Error

router = APIRouter(
    prefix='/storage',
    tags=['storage']
)


def is_object_exists(path_to_object: str) -> bool:
    try:
        if storage.stat_object(bucket_name, path_to_object) != None:
            return True
        else:
            return False
    except S3Error as e:
        return False

@router.get('/{user_id}/{filename}', response_class=FileResponse)
def get_file(user_id: int, filename: str):
    full_path = f'{user_id}/{filename}'
    try:
        # TODO: Find way for don't loading
        if storage.fget_object(bucket_name, full_path, filename) == None:
            raise FileNotFoundError()
        return FileResponse(filename)
    except:
        raise HTTPException(404, 'File not found')


@router.post('/{user_id}', response_model=FileUploadedScheme)
def add_file(user_id: int, file: UploadFile):
    # TODO: User is owner checking
    full_path = f'{user_id}/{file.filename}'
    if is_object_exists(full_path):
        raise HTTPException(409, 'File with this name already exists')
    try:
        storage.put_object(bucket_name, full_path, file.file, file.size)
        return FileUploadedScheme(
            url=router.url_path_for('get_file', user_id=user_id, filename=file.filename)  
        )
    except ValueError as e:
        raise HTTPException(409, 'Failed to upload file: ' + e.message)


@router.delete('/{user_id}/{filename}')
def delete_file(user_id: int, filename: str):
    # TODO: User is owner checking
    full_path = f'{user_id}/{filename}'
    if not is_object_exists(full_path):
        raise HTTPException(409, 'File doesn\'t exist')
    try:
        storage.remove_object(bucket_name, full_path)
        return {}
    except ValueError as e:
        raise HTTPException(404, 'Failed to delete file: ' + e.message)