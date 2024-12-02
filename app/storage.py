from minio import Minio

from .config import _settings

storage = Minio(
    _settings.minio_url,
    _settings.minio.LOGIN,
    _settings.minio.PASSWORD,
    secure=False
)