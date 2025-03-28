import os.path
from typing import AsyncGenerator, Iterator, Any
from fastapi import UploadFile
from minio import S3Error
from minio.datatypes import Object, BaseHTTPResponse
from minio.helpers import ObjectWriteResult

from app.core import get_settings, get_storage


__all__ = ["is_file_exists", "get_file_stream", "get_files_list", "upload_file", "delete_file"]


def is_file_exists(path_to_object: str) -> bool:
    try:
        return get_storage().stat_object(get_settings().minio.BUCKET_NAME, path_to_object) is not None
    except S3Error as e:
        return False


async def __file_stream_generator(file_response: BaseHTTPResponse) -> AsyncGenerator[bytes, Any]:
    try:
        for chunk in file_response.stream():
            yield chunk
    finally:
        file_response.close()
        file_response.release_conn()


def get_file_stream(full_path: str) -> AsyncGenerator[bytes, Any]:
    file_response = get_storage().get_object(get_settings().minio.BUCKET_NAME, full_path)
    return __file_stream_generator(file_response)


def get_files_list(user_id: int) -> Iterator[Object]:
    return get_storage().list_objects(get_settings().minio.BUCKET_NAME, f'{user_id}/')


def upload_file(user_id: int, file: UploadFile) -> ObjectWriteResult:
    full_path = f'{user_id}/{file.filename}'
    name, extension = os.path.splitext(file.filename)
    # TODO: Here can be some additional extension's checks
    index = 0
    while is_file_exists(full_path):
        index += 1
        full_path = f'{user_id}/{name}_{index}{extension}'
    return get_storage().put_object(
        get_settings().minio.BUCKET_NAME,
        full_path, file.file, file.size
    )


def delete_file(full_path: str) -> bool:
    get_storage().remove_object(get_settings().minio.BUCKET_NAME, full_path)
    return True
