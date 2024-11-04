from minio import Minio, S3Error
from os import getenv

bucket_name = getenv('MINIO_BUCKET_NAME')

storage = Minio(
    getenv('MINIO_HOSTNAME'),
    getenv('MINIO_LOGIN'),
    getenv('MINIO_PASSWORD'),
    secure=False
)


def is_object_exists(path_to_object: str) -> bool:
    try:
        if storage.stat_object(bucket_name, path_to_object) != None:
            return True
        else:
            return False
    except S3Error as e:
        return False