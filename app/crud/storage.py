from typing import Generator, Iterator, BinaryIO

from minio import S3Error
from minio.datatypes import Object
from minio.helpers import ObjectWriteResult

from app.config import minio_settings
from app.storage import storage


def is_file_exists(path_to_object: str) -> bool:
    try:
        if storage.stat_object(minio_settings.BUCKET_NAME, path_to_object) != None:
            return True
        else:
            return False
    except S3Error as e:
        return False


def get_file_stream(full_path: str) -> Generator[bytes, any, None]:
    file_response = storage.get_object(minio_settings.BUCKET_NAME, full_path)
    async def __file_stream_generator():
        try:
            for chunk in file_response.stream():
                yield chunk
        finally:
            file_response.close()
            file_response.release_conn()
    return __file_stream_generator()


def get_files_list(user_id: int) -> Iterator[Object]:
    return storage.list_objects(minio_settings.BUCKET_NAME, f'{user_id}/')


def upload_file(full_path: str, data: BinaryIO, size: int) -> ObjectWriteResult:
    return storage.put_object(minio_settings.BUCKET_NAME, full_path, data, size)


def delete_file(full_path: str):
    storage.remove_object(minio_settings.BUCKET_NAME, full_path)