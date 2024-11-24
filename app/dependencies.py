from typing import Annotated

from fastapi import Depends, Body
from sqlalchemy.ext.asyncio import AsyncConnection

from .auth import get_profile_id
from .database import get_db_async_connection

__all__ = ["DBConnection", "UserID", "IntList"]


DBConnection = Annotated[AsyncConnection, Depends(get_db_async_connection)]

UserID = Annotated[int, Depends(get_profile_id)]

IntList = Annotated[list[int], Body]
