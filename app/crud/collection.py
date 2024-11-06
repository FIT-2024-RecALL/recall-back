from sqlalchemy import select, insert
from sqlalchemy.ext.asyncio import AsyncConnection

from app.crud.user import check_user_id
from app.models import CollectionTable
from app.schemas.collection import Collection, CollectionCreate


async def get_collection(conn: AsyncConnection, collection_id: int):
    query = select(CollectionTable.c[*Collection.model_fields]).where(
        CollectionTable.c.id == collection_id
    )
    result = await conn.execute(query)
    return result.mappings().first()


async def get_collections(conn: AsyncConnection, limit: int, skip: int):
    query = (select(CollectionTable.c[*Collection.model_fields]).limit(limit)).offset(skip)
    result = await conn.execute(query)
    return result.mappings().all()


def get_collection_cards():
    pass


async def create_collection(conn: AsyncConnection, user_id: int, collection: CollectionCreate):
    await check_user_id(conn, user_id)
    query = insert(CollectionTable).values(owner_id=user_id, **collection.model_dump()
    ).returning(CollectionTable.c[*Collection.model_fields])

    result = await conn.execute(query)
    await conn.commit()
    return result.mappings().first()
