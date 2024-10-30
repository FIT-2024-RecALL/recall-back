from typing import Annotated

from fastapi import Depends
from sqlalchemy import Connection

from app.database import engine


def get_connection() -> Connection:
    with engine.connect() as conn:
        yield conn


DBConnection = Annotated[Connection, Depends(get_connection)]
