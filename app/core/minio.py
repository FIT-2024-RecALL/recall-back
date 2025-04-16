import os.path
from typing import AsyncGenerator, Any
from fastapi import UploadFile
from miniopy_async import Minio, S3Error
from miniopy_async.helpers import ObjectWriteResult
from miniopy_async.datatypes import ClientResponse, ClientSession

from .config import get_settings


__all__ = ["FileStream", "is_bucket_available", "is_file_uploaded", "get_file_stream", "upload_file", "delete_file"]


FileStream = AsyncGenerator[bytes, Any]


__settings = get_settings()

__storage = Minio(
    __settings.minio_url,
    __settings.minio.LOGIN,
    __settings.minio.PASSWORD,
    secure=False
)


async def is_bucket_available() -> bool:
    try:
        return await __storage.bucket_exists(__settings.minio.BUCKET_NAME)
    except ValueError:
        return False


async def is_file_uploaded(path_to_object: str) -> bool:
    try:
        return await __storage.stat_object(__settings.minio.BUCKET_NAME, path_to_object) is not None
    except S3Error as e:
        return False
    

async def upload_file(file: UploadFile) -> ObjectWriteResult:
    full_path = file.filename
    name, extension = os.path.splitext(file.filename)
    index = 0
    while await is_file_uploaded(full_path):
        index += 1
        full_path = f'{name}_{index}{extension}'
    return await __storage.put_object(
        __settings.minio.BUCKET_NAME,
        full_path, file.file, file.size
    )


async def __file_stream_generator(session: ClientSession, file_response: ClientResponse) -> FileStream:
    try:
        async for chunk, _ in file_response.content.iter_chunks():
            yield chunk
    finally:
        file_response.release()
        file_response.close()
        await session.close()


async def get_file_stream(full_path: str) -> FileStream | None:
    try:
        session = ClientSession()
        file_response = await __storage.get_object(__settings.minio.BUCKET_NAME, full_path, session)
        return __file_stream_generator(session, file_response)
    except S3Error:
        return None


async def delete_file(full_path: str) -> bool:
    await __storage.remove_object(__settings.minio.BUCKET_NAME, full_path)
    return True
