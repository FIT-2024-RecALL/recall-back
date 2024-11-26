from sqlalchemy import select, insert, exists, delete
from sqlalchemy.ext.asyncio import AsyncConnection

from app import CardTable
from app.schemas import Card, CardCreate

__all__ = ["check_card_id", "get_card", "get_cards", "create_card", "delete_card"]


async def check_card_id(conn: AsyncConnection, card_id: int):
    result = await conn.execute(select(exists().where(CardTable.c.id == card_id)))
    if not result.scalar():
        raise ValueError("Card not found")


async def get_card(conn: AsyncConnection, card_id: int):
    result = await conn.execute(
        select(CardTable.c[*Card.model_fields]).where(CardTable.c.id == card_id)
    )
    return result.mappings().first()


async def get_cards(conn: AsyncConnection, *, limit: int | None, skip: int):
    query = select(CardTable.c[*Card.model_fields]).offset(skip)
    if limit is not None:
        query = query.limit(limit)
    result = await conn.execute(query)
    return result.mappings().all()


async def create_card(conn: AsyncConnection, user_id: int,  card: CardCreate):
    result = await conn.execute(
        insert(CardTable).values(owner_id=user_id, **card.model_dump())
        .returning(CardTable.c[*Card.model_fields])
    )
    await conn.commit()
    return result.mappings().first()


async def delete_card(conn: AsyncConnection, card_id: int):
    await conn.execute(delete(CardTable).where(CardTable.c.id == card_id))
    await conn.commit()
