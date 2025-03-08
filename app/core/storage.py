from minio import Minio

from .config import get_settings


storage = Minio(
    get_settings().minio_url,
    get_settings().minio.LOGIN,
    get_settings().minio.PASSWORD,
    secure=False
)
