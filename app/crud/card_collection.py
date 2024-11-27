from sqlalchemy import select, insert, delete
from sqlalchemy.ext.asyncio import AsyncConnection

from app import CardTable, CardCollectionTable, CollectionTable
from app.schemas import Card, Collection

__all__ = [
    "get_user_collection_cards", "get_user_card_collections", "create_card_collection_connections",
]


async def get_user_collection_cards(
        conn: AsyncConnection, user_id: int, collection_id: int
) -> list[Card]:
    query = select(CardTable.c[*Card.model_fields]).join(
        CardCollectionTable, CardTable.c.id == CardCollectionTable.c.card_id
    ).where(
        CardTable.c.owner_id == user_id, CardCollectionTable.c.collection_id == collection_id
    )
    result = await conn.execute(query)
    return list(map(lambda x: Card(**x), result.mappings().all()))


async def get_user_card_collections(
        conn: AsyncConnection, user_id: int, card_id: int
) -> list[Collection]:
    query = select(CollectionTable.c[*Collection.model_fields]).join(
        CardCollectionTable, CollectionTable.c.id == CardCollectionTable.c.collection_id
    ).where(
        CollectionTable.c.owner_id == user_id, CardCollectionTable.c.card_id == card_id
    )
    result = await conn.execute(query)
    return list(map(lambda x: Collection(**x), result.mappings().all()))


async def _fetch_exist_collections(conn: AsyncConnection, collections: list[int]) -> list[int]:
    exist_unique_collections = await conn.execute(
        select(CollectionTable.c.id).where(CollectionTable.c.id.in_(set(collections)))
    )
    return list(exist_unique_collections.scalars())


async def _set_card_collection_connections(
        conn: AsyncConnection, card_id: int, collections: list[int]
) -> None:
    await conn.execute(
        insert(CardCollectionTable),
        [{"card_id": card_id, "collection_id": collection_id} for collection_id in collections],
    )
    await conn.commit()


async def create_card_collection_connections(
        conn: AsyncConnection, card_id: int, collections: list[int]
) -> None:
    new_collections: list[int] = await _fetch_exist_collections(conn, collections)
    if len(new_collections) < 1:
        raise ValueError("Collections not found")
    await _set_card_collection_connections(conn, card_id, new_collections)


async def update_card_collection_connections():
    ...

###########################################################################################################
async def sift_exist_connections(conn: AsyncConnection, collection_id: int, cards: list[int]) -> list[int]:
    unique_cards: list[int] = list(set(cards))
    query = select(CardCollectionTable.c.card_id).where(
        CardCollectionTable.c.collection_id == collection_id,
        CardCollectionTable.c.card_id.in_(unique_cards)
    )
    collection_unique_cards = await conn.execute(query)
    return [x[0] for x in collection_unique_cards.all()]


##############################################################################################
async def create_card_collection(conn: AsyncConnection, collection_id: int, cards: list[int]):
    exist_connections = await sift_exist_connections(conn, collection_id, cards)
    new_connections: list[int] = [x for x in cards if x not in exist_connections]
    if not new_connections:
        return
    existing_cards = []#await sift_exist_cards(conn, new_connections)
    if not existing_cards:
        return

    await conn.execute(
        insert(CardCollectionTable),
        [{"card_id": card_id, "collection_id": collection_id} for card_id in existing_cards],
    )
    await conn.commit()
 

##############################################################################################
async def delete_card_collection(conn: AsyncConnection, collection_id: int, cards: list[int]):
    exist_connections: list[int] = await sift_exist_connections(conn, collection_id, cards)
    query = delete(CardCollectionTable).where(
        CardCollectionTable.c.collection_id == collection_id,
        CardCollectionTable.c.card_id.in_(exist_connections)
    )
    await conn.execute(query)
    await conn.commit()
