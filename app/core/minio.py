import os.path
from typing import AsyncGenerator, Iterator, Any
from fastapi import UploadFile
from minio import Minio, S3Error
from minio.datatypes import Object, BaseHTTPResponse
from minio.helpers import ObjectWriteResult

from .config import get_settings


__all__ = ["FileStream", "is_file_uploaded", "get_file_stream", "get_files_list", "upload_file", "delete_file"]


type FileStream = AsyncGenerator[bytes, Any]


__storage = Minio(
    get_settings().minio_url,
    get_settings().minio.LOGIN,
    get_settings().minio.PASSWORD,
    secure=False
)


def is_file_uploaded(path_to_object: str) -> bool:
    try:
        return __storage.stat_object(get_settings().minio.BUCKET_NAME, path_to_object) is not None
    except S3Error as e:
        return False
    

def upload_file(file: UploadFile) -> ObjectWriteResult:
    full_path = file.filename
    name, extension = os.path.splitext(file.filename)
    index = 0
    while is_file_uploaded(full_path):
        index += 1
        full_path = f'{name}_{index}{extension}'
    return __storage.put_object(
        get_settings().minio.BUCKET_NAME,
        full_path, file.file, file.size
    )


async def __file_stream_generator(file_response: BaseHTTPResponse) -> FileStream:
    try:
        for chunk in file_response.stream():
            yield chunk
    finally:
        file_response.close()
        file_response.release_conn()


def get_file_stream(full_path: str) -> FileStream:
    file_response = __storage.get_object(get_settings().minio.BUCKET_NAME, full_path)
    return __file_stream_generator(file_response)


def get_files_list(user_id: int) -> Iterator[Object]:
    return __storage.list_objects(get_settings().minio.BUCKET_NAME, f'{user_id}/')


def delete_file(full_path: str) -> bool:
    __storage.remove_object(get_settings().minio.BUCKET_NAME, full_path)
    return True
