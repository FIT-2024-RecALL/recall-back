from sqlalchemy.ext.asyncio import create_async_engine

from app.core.config import _settings

from .models import get_metadata


__all__ = ["create_db_tables", "get_db_engine", "close_db_connections", "delete_tables"]


## магические константы надо будет перенести в конфиг
__engine = create_async_engine(
    url=_settings.db_url_asyncpg,
    pool_size=10,
    max_overflow=2,
    pool_recycle=1800,  # в секундах
    pool_pre_ping=True,
    echo=True,
)


async def create_db_tables():
    async with __engine.begin() as conn:
        await conn.run_sync(get_metadata().create_all)


## shell: python -c "import asyncio; from app.database import delete_tables; asyncio.run(delete_tables())"
async def delete_tables() -> None:
    async with __engine.begin() as conn:
        await conn.run_sync(get_metadata().drop_all)


async def close_db_connections():
    await __engine.dispose()


def get_db_engine():
    return __engine
