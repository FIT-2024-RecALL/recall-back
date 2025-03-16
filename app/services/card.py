from app.db import UnitOfWork
from app.repositories import CardRepository
from app.schemas import Card, CardCreate


"""
async def create_card(conn: AsyncConnection, user_id: int, card: CardCreate) -> Card:
    result = await conn.execute(
        insert(CardTable).values(owner_id=user_id, **card.model_dump())
        .returning(CardTable.c[*Card.model_fields])
    )
    await conn.commit()
    return Card(**result.mappings().first())
    
async def get_card(conn: AsyncConnection, card_id: int) -> Card | None:
    result = (await conn.execute(
        select(CardTable.c[*Card.model_fields]).where(CardTable.c.id == card_id)
    )).mappings().first()
    return result if result is None else Card(**result)

"""


class CardService:
    async def create_card(self, uow: UnitOfWork, user_id: int, card: CardCreate) -> Card:
        card_repo = uow.get_repository(CardRepository)
        card_data = card.model_dump()
        card_data["owner_id"] = user_id
        return await card_repo.create_one(card_data, Card)
