from sqlalchemy import select, insert, delete, update, exists
from sqlalchemy.ext.asyncio import AsyncConnection

from app.db.models import CardTable
from app.schemas import Card, CardCreate


__all__ = [
    "check_card_id", "check_user_card_id", "get_card", "get_cards", "get_user_cards",
    "create_card", "delete_card", "update_card", "delete_cards"
]


async def check_card_id(conn: AsyncConnection, card_id: int) -> None:
    result = await conn.execute(select(exists().where(CardTable.c.id == card_id)))
    if not result.scalar():
        raise ValueError("Card not found")


async def check_user_card_id(conn: AsyncConnection, user_id: int, card_id: int) -> None:
    result = await conn.execute(select(CardTable.c.owner_id).where(
        CardTable.c.id == card_id).limit(1)
    )
    owner_id: int | None = result.scalar()
    if owner_id is None or owner_id != user_id:
        raise ValueError("Card not found in User collections")


async def get_card(conn: AsyncConnection, card_id: int) -> Card | None:
    result = (await conn.execute(
        select(CardTable.c[*Card.model_fields]).where(CardTable.c.id == card_id)
    )).mappings().first()
    return result if result is None else Card(**result)


async def get_cards(conn: AsyncConnection, *, limit: int | None, skip: int) -> list[Card]:
    query = select(CardTable.c[*Card.model_fields]).offset(skip)
    if limit is not None:
        query = query.limit(limit)
    result = await conn.execute(query)
    return [Card(**card) for card in result.mappings().all()]


async def get_user_cards(conn: AsyncConnection, user_id: int, *, limit: int | None, skip: int) -> list[int]:
    query = select(CardTable.c.id).where(
        CardTable.c.owner_id == user_id).offset(skip)
    if limit is not None:
        query = query.limit(limit)
    result = await conn.execute(query)
    return list(result.scalars().all())


async def create_card(conn: AsyncConnection, user_id: int, card: CardCreate) -> Card:
    result = await conn.execute(
        insert(CardTable).values(owner_id=user_id, **card.model_dump())
        .returning(CardTable.c[*Card.model_fields])
    )
    await conn.commit()
    return Card(**result.mappings().first())


async def delete_card(conn: AsyncConnection, card_id: int) -> None:
    await conn.execute(delete(CardTable).where(CardTable.c.id == card_id))
    await conn.commit()


async def delete_cards(conn: AsyncConnection, cards: list[int]) -> None:
    await conn.execute(delete(CardTable).where(CardTable.c.id.in_(cards)))
    await conn.commit()


async def update_card(conn: AsyncConnection, card_id: int, card: CardCreate) -> Card:
    result = await conn.execute(
        update(CardTable).where(CardTable.c.id == card_id).values(**card.model_dump())
        .returning(CardTable.c[*Card.model_fields])
    )
    await conn.commit()
    return Card(**result.mappings().first())
