from sqlalchemy import MetaData
from sqlalchemy.ext.asyncio import create_async_engine

from app.config import dbSettings


engine = create_async_engine(url=dbSettings.db_url_asyncpg, echo=True)

metadata = MetaData()

async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(metadata.create_all)
