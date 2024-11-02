from minio import Minio
from os import getenv

bucket_name = getenv('MINIO_BUCKET_NAME')

storage = Minio(
    getenv('MINIO_HOSTNAME'),
    getenv('MINIO_LOGIN'),
    getenv('MINIO_PASSWORD'),
    secure=False
)