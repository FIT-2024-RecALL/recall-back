from sqlalchemy import select, insert
from sqlalchemy.ext.asyncio import AsyncConnection

from app.models import CardTable
from app.schemas.card import Card, CardCreate


async def get_card(conn: AsyncConnection, card_id: int):
    query = select(CardTable.c[*Card.model_fields]).where(
        CardTable.c.id == card_id
    )
    result = await conn.execute(query)
    return result.mappings().first()


async def get_cards(conn: AsyncConnection, *, limit: int, skip: int):
    query = select(CardTable.c[*Card.model_fields]).limit(limit).offset(skip)
    result = await conn.execute(query)
    return result.mappings().all()


async def create_card(conn: AsyncConnection, card: CardCreate):
    query = insert(CardTable).values(**card.model_dump()).returning(
        CardTable.c[*Card.model_fields]
    )
    result = await conn.execute(query)
    await conn.commit()
    return result.mappings().first()
