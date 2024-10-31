from fastapi import APIRouter, HTTPException

from app import crud, schemas
from app.dependencies import DBConnection


router = APIRouter(
    prefix="/cards",
    tags=["card"]
)


@router.get("/{card_id}", response_model=schemas.card.Card)
def read_card(conn: DBConnection, card_id: int):
    card = crud.card.get_card(conn, card_id)
    if card is None:
        raise HTTPException(status_code=404, detail="Card not found")
    return card


@router.get("/", response_model=list[schemas.card.Card])
def read_cards(conn: DBConnection, limit: int = 100, skip: int = 0):
    return crud.card.get_cards(conn, limit=limit, skip=skip)


@router.post("/", response_model=schemas.card.Card)
def create_card(conn: DBConnection, card: schemas.card.CardCreate):
    return crud.card.create_card(conn, card)
