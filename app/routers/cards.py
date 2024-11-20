from fastapi import APIRouter, HTTPException, Response

from app import auth
from app import crud
from app.dependencies import DBConnection, JWToken
from app.schemas.card import Card, CardCreate


router = APIRouter(
    prefix="/cards",
    tags=["card"]
)


@router.get("/{card_id}", response_model=Card)
async def read_card(conn: DBConnection, card_id: int):
    card = await crud.card.get_card(conn, card_id)
    if card is None:
        raise HTTPException(status_code=404, detail="Card not found")
    return card


@router.get("/", response_model=list[Card])
async def read_cards(conn: DBConnection, skip: int = 0, limit: int | None = None):
    return await crud.card.get_cards(conn, limit=limit, skip=skip)


@router.post("/", response_model=Card)
async def create_card(conn: DBConnection, token: JWToken, card: CardCreate):
    try:
        user_id: int = auth.utils.get_profile_id(token)
        return await crud.card.create_card(conn, user_id, card)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/{card_id}", response_class=Response)
async def delete_card(conn: DBConnection, card_id: int):
    try:
        await crud.card.check_card_id(conn, card_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    await crud.card.delete_card(conn, card_id)
    await crud.card_collection.delete_card_collection_by_card(conn, card_id)
    await crud.train_record.delete_train_record_by_card(conn, card_id)
    return Response(status_code=200)
