from typing import Annotated

from fastapi import Depends, Body
from sqlalchemy import Connection

from minio import Minio

from app.database import engine
from app.storage import storage


def get_connection() -> Connection:
    with engine.connect() as conn:
        yield conn


def get_storage() -> Minio:
    return storage


DBConnection = Annotated[Connection, Depends(get_connection)]

IntList = Annotated[list[int], Body]

StorageConnection = Annotated[Minio, Depends(get_storage)]
