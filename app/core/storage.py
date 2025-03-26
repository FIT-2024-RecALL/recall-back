from minio import Minio

from .config import get_settings


__all__ = ["get_storage"]


__storage = Minio(
    get_settings().minio_url,
    get_settings().minio.LOGIN,
    get_settings().minio.PASSWORD,
    secure=False
)

def get_storage() -> Minio:
    return __storage
