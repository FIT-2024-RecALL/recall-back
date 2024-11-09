from sqlalchemy import select, insert, exists
from sqlalchemy.ext.asyncio import AsyncConnection

from app.crud.user import check_user_id
from app.models import CardTable
from app.schemas.card import Card, CardCreate


async def check_card_id(conn: AsyncConnection, card_id: int):
    query = select(exists().where(CardTable.c.id == card_id))
    result = await conn.execute(query)
    if not result.scalar():
        raise ValueError("Card with this id doesn't exist")


async def get_card(conn: AsyncConnection, card_id: int):
    query = select(CardTable.c[*Card.model_fields]).where(CardTable.c.id == card_id)
    result = await conn.execute(query)
    return result.mappings().first()


async def get_cards(conn: AsyncConnection, *, limit: int | None, skip: int):
    query = select(CardTable.c[*Card.model_fields]).offset(skip)
    if limit is not None:
        query = query.limit(limit)
    result = await conn.execute(query)
    return result.mappings().all()


async def create_card(conn: AsyncConnection, user_id: int,  card: CardCreate):
    await check_user_id(conn, user_id)
    query = (insert(CardTable).values(owner_id=user_id, **card.model_dump())
             .returning(CardTable.c[*Card.model_fields]))

    result = await conn.execute(query)
    await conn.commit()
    return result.mappings().first()
