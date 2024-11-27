from fastapi import APIRouter, HTTPException, Response

from app import crud, DBConnection, IntList, UserID
from app.schemas import Card, CardCreate


router = APIRouter(
    prefix="/cards",
    tags=["card"]
)


### ПЕРЕПИСАТЬ ДЛЯ ПОЛЬЗОВАТЕЛЯ
@router.get("/{card_id}", response_model=Card)
async def read_card(conn: DBConnection, card_id: int):
    card = await crud.get_card(conn, card_id)
    if card is None:
        raise HTTPException(status_code=404, detail="Card not found")
    return card


### ПЕРЕПИСТАЬ ДЛЯ ПОЛЬЗОВАТЕЛЯ
@router.get("/", response_model=list[Card])
async def read_cards(conn: DBConnection, skip: int = 0, limit: int | None = None):
    return await crud.get_cards(conn, limit=limit, skip=skip)


@router.post("/", response_model=Card)
async def create_card(conn: DBConnection, user_id: UserID, card: CardCreate, collections: IntList) -> Card:
    result_card: Card = await crud.create_card(conn, user_id, card)
    try:
        await crud.check_user_id(conn, user_id)
        await crud.create_card_collection_connections(conn, result_card.id, collections)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    return result_card


@router.delete("/{card_id}", response_class=Response)
async def delete_card(conn: DBConnection, user_id: UserID, card_id: int):
    try:
        await crud.check_user_id(conn, user_id)
        await crud.check_card_id(conn, user_id, card_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    await crud.delete_user_card(conn, user_id, card_id)
    return Response(status_code=200)


@router.put("/{card_id}", response_class=Response)
async def update_card():
    ...
