from typing import Annotated

from fastapi import Depends, Body
from sqlalchemy.ext.asyncio import AsyncConnection

from minio import Minio

from app.database import get_async_connection


DBConnection = Annotated[AsyncConnection, Depends(get_async_connection)]
IntList = Annotated[list[int], Body]

StorageConnection = Annotated[Minio, Depends(get_storage)]
