from typing import Annotated
from fastapi import Depends, Body
from sqlalchemy.ext.asyncio import AsyncConnection

from app.core import get_profile_id
from app.db.database import get_db_async_connection, get_db_async_transaction


__all__ = ["DBConnection", "DBTransaction", "UserID", "IntList"]


DBConnection = Annotated[AsyncConnection, Depends(get_db_async_connection)]
DBTransaction = Annotated[AsyncConnection, Depends(get_db_async_transaction)]

UserID = Annotated[int, Depends(get_profile_id)]

IntList = Annotated[list[int], Body(min_length=1, max_length=100)]
