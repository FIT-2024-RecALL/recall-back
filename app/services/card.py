from app.db import UnitOfWork
from app.repositories import CardRepository
from app.schemas import Card, CardCreate


class CardService:
    pass


"""
async def create_card(conn: AsyncConnection, user_id: int, card: CardCreate) -> Card:
    result = await conn.execute(
        insert(CardTable).values(owner_id=user_id, **card.model_dump())
        .returning(CardTable.c[*Card.model_fields])
    )
    await conn.commit()
    return Card(**result.mappings().first())

@router.post("/", response_model=Card)
async def create_card(
        conn: DBConnection, user_id: UserID, card: CardCreate, collections: IntList
) -> Card:
    try:
        await repositories.check_user_id(conn, user_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    result_card: Card = await repositories.create_card(conn, user_id, card)
    try:
        await repositories.create_card_collection_connections(conn, user_id, result_card.id, collections)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    return result_card
"""

""" 
async def get_card(conn: AsyncConnection, card_id: int) -> Card | None:
    result = (await conn.execute(
        select(CardTable.c[*Card.model_fields]).where(CardTable.c.id == card_id)
    )).mappings().first()
    return result if result is None else Card(**result)

@router.get("/{card_id}", response_model=Card)
async def read_card(conn: DBConnection, card_id: int):
    card: Card | None = await repositories.get_card(conn, card_id)
    if card is None:
        raise HTTPException(status_code=404, detail="Card not found")
    return card
"""
