from sqlalchemy.ext.asyncio import AsyncConnection, create_async_engine

from .config import _settings
from .models import _metadata

__all__ = ["create_db_tables", "close_db_connections", "get_db_async_connection"]


__engine = create_async_engine(url=_settings.db_url_asyncpg, echo=True)

async def create_db_tables():
    async with __engine.begin() as conn:
        await conn.run_sync(_metadata.create_all)


async def close_db_connections():
    await __engine.dispose()


async def get_db_async_connection() -> AsyncConnection:
    async with __engine.connect() as conn:
        yield conn
        await conn.close()
