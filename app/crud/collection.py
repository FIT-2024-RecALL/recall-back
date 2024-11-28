from sqlalchemy import select, insert, delete, update
from sqlalchemy.ext.asyncio import AsyncConnection

from app import CollectionTable
from app.schemas import Collection, CollectionCreate

__all__ = [
    "check_collection_id", "get_collection", "get_collections", "create_collection",
    "get_user_collections", "delete_collection", "update_collection"
]


async def check_collection_id(conn: AsyncConnection, user_id: int, collection_id: int):
    result = await conn.execute(
        select(CollectionTable.c.owner_id).where(CollectionTable.c.id == collection_id).limit(1)
    )
    owner_id: int | None = result.scalar()
    if owner_id is None or owner_id != user_id:
        raise ValueError("User does not have this collection")


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


async def get_user_collections(
        conn: AsyncConnection, user_id: int, limit: int | None, skip: int
) -> list[Collection]:
    query = select(CollectionTable.c[*Collection.model_fields]).where(
        CollectionTable.c.owner_id == user_id).offset(skip)
    if limit is not None:
        query = query.limit(limit)
    result = await conn.execute(query)
    return [Collection(**collection) for collection in result.mappings().all()]


async def create_collection(conn: AsyncConnection, user_id: int, collection: CollectionCreate):
    query = (insert(CollectionTable).values(owner_id=user_id, **collection.model_dump())
             .returning(CollectionTable.c[*Collection.model_fields]))
    result = await conn.execute(query)
    await conn.commit()
    return result.mappings().first()


async def delete_collection(conn: AsyncConnection, collection_id: int) -> None:
    await conn.execute(delete(CollectionTable).where(CollectionTable.c.id == collection_id))
    await conn.commit()


async def update_collection(
        conn: AsyncConnection, collection_id: int, collection: CollectionCreate
) -> Collection:
    result = await conn.execute(
        update(CollectionTable).where(
            CollectionTable.c.id == collection_id).values(**collection.model_dump()
        ).returning(CollectionTable.c[*Collection.model_fields])
    )
    await conn.commit()
    return Collection(**result.mappings().first())
