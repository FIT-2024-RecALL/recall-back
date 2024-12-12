from sqlalchemy.ext.asyncio import AsyncConnection, create_async_engine

from .config import _settings
from .models import _metadata

__all__ = ["create_db_tables", "get_db_async_connection", "get_db_async_transaction",
           "close_db_connections", "delete_tables"]


__engine = create_async_engine(url=_settings.db_url_asyncpg, echo=True)

async def create_db_tables():
    async with __engine.begin() as conn:
        await conn.run_sync(_metadata.create_all)


## shell: python -c "import asyncio; from app import delete_tables; asyncio.run(delete_tables())"
async def delete_tables() -> None:
    async with __engine.begin() as conn:
        await conn.run_sync(_metadata.drop_all)


async def close_db_connections():
    await __engine.dispose()


async def get_db_async_connection() -> AsyncConnection:
    async with __engine.connect() as conn:
        yield conn


async def get_db_async_transaction() -> AsyncConnection:
    async with __engine.begin() as trans:
        yield trans
