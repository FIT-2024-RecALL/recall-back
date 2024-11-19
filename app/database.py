from sqlalchemy.ext.asyncio import AsyncConnection, create_async_engine

from app.config import settings
from app.models import metadata


__engine = create_async_engine(url=settings.db_url_asyncpg, echo=True)

async def create_tables():
    async with __engine.begin() as conn:
        await conn.run_sync(metadata.create_all)

async def close_connections():
    await __engine.dispose()

async def get_async_connection() -> AsyncConnection:
    async with __engine.connect() as conn:
        yield conn
        await conn.close()
