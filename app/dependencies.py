from typing import Annotated

from fastapi import Depends, Body
from sqlalchemy.ext.asyncio import AsyncConnection

from app import get_db_async_connection
from app.auth import get_token, get_profile_id

__all__ = ["DBConnection", "JWToken", "UserID", "IntList"]


DBConnection = Annotated[AsyncConnection, Depends(get_db_async_connection)]

JWToken = Annotated[str, Depends(get_token)]

UserID = Annotated[int, Depends(get_profile_id)]

IntList = Annotated[list[int], Body]
