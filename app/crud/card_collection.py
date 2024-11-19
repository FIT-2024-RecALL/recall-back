from sqlalchemy import select, insert, delete
from sqlalchemy.ext.asyncio import AsyncConnection
from sqlalchemy.orm.collections import collection

from app.crud.collection import check_collection_id
from app.models import CardTable, CardCollectionTable
from app.schemas.card import Card


async def get_collection_cards(conn: AsyncConnection, collection_id: int):
    await check_collection_id(conn, collection_id)
    query = select(CardTable.c[*Card.model_fields]).where(
        CardTable.c.id == CardCollectionTable.c.card_id,
        CardCollectionTable.c.collection_id == collection_id
    )
    result = await conn.execute(query)
    return result.mappings().all()


def get_card_collections():
    pass


async def sift_exist_connections(conn: AsyncConnection, collection_id: int, cards: list[int]) -> list[int]:
    unique_cards: list[int] = list(set(cards))
    query = select(CardCollectionTable.c.card_id).where(
        CardCollectionTable.c.collection_id == collection_id,
        CardCollectionTable.c.card_id.in_(unique_cards)
    )
    collection_unique_cards = await conn.execute(query)
    return [x[0] for x in collection_unique_cards.all()]


async def sift_exist_cards(conn: AsyncConnection, cards: list[int]):
    unique_cards: list[int] = list(set(cards))
    query = select(CardTable.c.id).where(CardTable.c.id.in_(unique_cards))
    exist_unique_cards = await conn.execute(query)
    return [x[0] for x in exist_unique_cards.all()]


# Можно переписать через подзапрос (Deep Alchemy)
async def create_card_collection(conn: AsyncConnection, collection_id: int, cards: list[int]):
    await check_collection_id(conn, collection_id)
    exist_connections = await sift_exist_connections(conn, collection_id, cards)
    new_connections: list[int] = [x for x in cards if x not in exist_connections]
    if not new_connections:
        return

    existing_cards = await sift_exist_cards(conn, new_connections)
    if not existing_cards:
        return

    await conn.execute(
        insert(CardCollectionTable),
        [
            {"card_id": card_id, "collection_id": collection_id}
            for card_id in existing_cards
        ],
    )
    await conn.commit()


async def delete_card_collection(conn: AsyncConnection, collection_id: int, cards: list[int]):
    exist_connections: list[int] = await sift_exist_connections(conn, collection_id, cards)
    query = delete(CardCollectionTable).where(
        CardCollectionTable.c.collection_id == collection_id,
        CardCollectionTable.c.card_id.in_(exist_connections)
    )
    await conn.execute(query)
    await conn.commit()
