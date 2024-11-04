from fastapi import APIRouter, HTTPException, UploadFile
from fastapi.responses import FileResponse, StreamingResponse
from urllib.parse import quote

from app.storage import storage, bucket_name, is_object_exists
from app.schemas.storage import FileUploadedScheme

router = APIRouter(
    prefix='/storage',
    tags=['storage']
)

@router.get('/{user_id}/{filename}', response_class=StreamingResponse)
def get_file(user_id: int, filename: str):
    full_path = f'{user_id}/{filename}'
    try:
        file_response = storage.get_object(bucket_name, full_path)
        async def file_stream_generator():
            try:
                for chunk in file_response.stream():
                    yield chunk
            finally:
                file_response.close()
                file_response.release_conn()
        return StreamingResponse(
            file_stream_generator(),
            media_type="application/octet-stream",
            headers={"Content-Disposition": f"attachment; filename={filename}"}
        )
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
            url=router.url_path_for('get_file', user_id=user_id, filename=quote(file.filename))
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