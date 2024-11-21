from minio import Minio

from app.config import minio_settings

storage = Minio(
    minio_settings.url,
    minio_settings.LOGIN,
    minio_settings.PASSWORD,
    secure=False
)