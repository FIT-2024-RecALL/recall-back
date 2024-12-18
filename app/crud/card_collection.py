from sqlalchemy import select, insert, delete
from sqlalchemy.ext.asyncio import AsyncConnection

from app.models import CardCollectionTable, CollectionTable
from app.schemas import CollectionShort

__all__ = [
    "get_collection_cards", "get_user_card_collections", "create_card_collection_connections",
    "update_card_collection_connections"
]


async def get_collection_cards(
        conn: AsyncConnection, collection_id: int
) -> list[int]:
    query = select(CardCollectionTable.c.card_id).where(
        CardCollectionTable.c.collection_id == collection_id
    )
    return list((await conn.execute(query)).scalars().all())


async def get_user_card_collections(
        conn: AsyncConnection, user_id: int, card_id: int
) -> list[CollectionShort]:
    query = select(CollectionTable.c[*CollectionShort.model_fields]).join(
        CardCollectionTable, CollectionTable.c.id == CardCollectionTable.c.collection_id
    ).where(
        CollectionTable.c.owner_id == user_id, CardCollectionTable.c.card_id == card_id
    )
    result = await conn.execute(query)
    return [CollectionShort(**collection) for collection in result.mappings().all()]


async def _fetch_exist_user_collections(
        conn: AsyncConnection, user_id: int, collections: list[int]
) -> list[int]:
    exist_unique_collections = await conn.execute(
        select(CollectionTable.c.id).where(
            CollectionTable.c.id.in_(set(collections)), CollectionTable.c.owner_id == user_id
        )
    )
    return list(exist_unique_collections.scalars().all())


async def _set_card_collection_connections(
        conn: AsyncConnection, card_id: int, collections: list[int]
) -> None:
    await conn.execute(
        insert(CardCollectionTable),
        [{"card_id": card_id, "collection_id": collection_id} for collection_id in collections],
    )
    await conn.commit()


async def create_card_collection_connections(
        conn: AsyncConnection, user_id: int, card_id: int, collections: list[int]
) -> None:
    new_collections = await _fetch_exist_user_collections(conn, user_id, collections)
    if not new_collections:
        raise ValueError("Collections not found")
    await _set_card_collection_connections(conn, card_id, new_collections)


async def _fetch_card_collections(conn: AsyncConnection, card_id: int) -> list[int]:
    card_collection_connections = await conn.execute(
        select(CardCollectionTable.c.collection_id).where(CardCollectionTable.c.card_id == card_id)
    )
    return list(card_collection_connections.scalars().all())


async def _unset_card_collection_connections(
        conn: AsyncConnection, card_id: int, collections: list[int]
) -> None:
    await conn.execute(
        delete(CardCollectionTable).where(
            CardCollectionTable.c.card_id == card_id,
            CardCollectionTable.c.collection_id.in_(collections)
        )
    )
    await conn.commit()


async def update_card_collection_connections(
        conn: AsyncConnection, user_id: int, card_id: int, collections: list[int]
) -> None:
    request_collections: set[int] = set(await _fetch_exist_user_collections(conn, user_id, collections))
    if not request_collections:
        raise ValueError("Collections not found")
    old_collections: set[int] = set(await _fetch_card_collections(conn, card_id))
    delete_collections: list[int] = list(old_collections.difference(request_collections))
    new_collections: list[int] = list(request_collections.difference(old_collections))
    if delete_collections:
        await _unset_card_collection_connections(conn, card_id, delete_collections)
    if new_collections:
        await _set_card_collection_connections(conn, card_id, new_collections)
