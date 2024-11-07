from typing import Annotated

from fastapi import Depends, Body
from sqlalchemy.ext.asyncio import AsyncConnection

from app.database import get_async_connection
from app.auth.utils import get_token


DBConnection = Annotated[AsyncConnection, Depends(get_async_connection)]
JWToken = Annotated[str, Depends(get_token)]
IntList = Annotated[list[int], Body]
