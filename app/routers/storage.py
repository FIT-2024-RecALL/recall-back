from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse
import os

from app.storage import storage, bucket_name

router = APIRouter(
    prefix='/storage',
    tags=['storage']
)



@router.get('/{path}', response_class=FileResponse)
def get_file(path: str):
    # response = None
    # try:
    #   response = m.get_object('recall-bucket', path)
    #   return response
    # finally:
    #   if response != None:
    #     response.close()
    #     response.release_conn()
    metadata = storage.fget_object(bucket_name, path, path) == None
    if metadata == None:
        return HTTPException(404, 'File not found')
    try:
        return FileResponse(path)
    finally:
        os.remove(path) # Doesn't work at all...


@router.delete('/{path}')
def delete_file(path: str):
    storage.remove_object(bucket_name, path)