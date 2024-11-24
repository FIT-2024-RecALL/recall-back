from sqlalchemy import select, insert, exists
from sqlalchemy.ext.asyncio import AsyncConnection

from app import CollectionTable
from app.crud import check_user_id
from app.schemas import Collection, CollectionCreate

__all__ = ["check_collection_id", "get_collection", "get_collections", "create_collection"]


async def check_collection_id(conn: AsyncConnection, collection_id: int):
    query = select(exists().where(CollectionTable.c.id == collection_id))
    result = await conn.execute(query)
    if not result.scalar():
        raise ValueError("Collection with this id doesn't exist")


async def get_collection(conn: AsyncConnection, collection_id: int):
    query = select(CollectionTable.c[*Collection.model_fields]).where(
        CollectionTable.c.id == collection_id
    )
    result = await conn.execute(query)
    return result.mappings().first()


async def get_collections(conn: AsyncConnection, limit: int | None, skip: int):
    query = select(CollectionTable.c[*Collection.model_fields]).offset(skip)
    if limit is not None:
        query = query.limit(limit)
    result = await conn.execute(query)
    return result.mappings().all()


async def create_collection(conn: AsyncConnection, user_id: int, collection: CollectionCreate):
    await check_user_id(conn, user_id) ## Может вынести это в route?

    query = (insert(CollectionTable).values(owner_id=user_id, **collection.model_dump())
             .returning(CollectionTable.c[*Collection.model_fields]))

    result = await conn.execute(query)
    await conn.commit()
    return result.mappings().first()
