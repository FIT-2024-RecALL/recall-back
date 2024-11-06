from fastapi import APIRouter, HTTPException

from app import crud
from app.dependencies import DBConnection
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
async def read_cards(conn: DBConnection, limit: int = 100, skip: int = 0):
    return await crud.card.get_cards(conn, limit=limit, skip=skip)


@router.post("/", response_model=Card)
async def create_card(conn: DBConnection, card: CardCreate):
    return await crud.card.create_card(conn, card)
