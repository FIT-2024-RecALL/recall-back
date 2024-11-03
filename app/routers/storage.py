from fastapi import APIRouter, HTTPException, UploadFile
from fastapi.responses import FileResponse

import os

from app.storage import storage, bucket_name
from app.schemas.storage import FileUploadedScheme

router = APIRouter(
    prefix='/storage',
    tags=['storage']
)


@router.get('/{path}', response_class=FileResponse)
def get_file(path: str):
    try:
        if storage.fget_object(bucket_name, path, path) == None:
            raise FileNotFoundError()
        return FileResponse(path)
    except:
        raise HTTPException(404, 'File not found')


@router.post('/{path}', response_model=FileUploadedScheme)
def add_file(file: UploadFile):
    try:
        if storage.stat_object(bucket_name, file.filename) != None:
            raise HTTPException(409, 'File with this name already exists')
        result = storage.put_object(bucket_name, file.filename, file.file, file.size)
        return FileUploadedScheme(
            url=router.url_path_for('add_file', path=result.object_name)  
        )
    except ValueError as e:
        raise HTTPException(409, 'Failed to upload file: ' + e.message)


@router.delete('/{path}')
def delete_file(path: str):
    try:
        storage.remove_object(bucket_name, path)
        return {}
    except ValueError as e:
        raise HTTPException(404, 'Failed to delete file: ' + e.message)