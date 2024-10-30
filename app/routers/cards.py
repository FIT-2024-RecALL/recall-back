"""from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import schemas


router = APIRouter(
    prefix="/cards",
    tags=["card"]
)


@router.post("/", response_model=schemas.card.Card)
def create_card(card: schemas.card.CardCreate, db: Session = Depends(get_db)):
    return crud.card.create_card(db=db, card=card)


@router.get("/", response_model=list[schemas.card.Card])
def read_cards(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.card.get_cards(db, skip=skip, limit=limit)


@router.get("/{card_id}", response_model=schemas.card.Card)
def read_card(card_id: int, db: Session = Depends(get_db)):
    db_card = crud.collection.get_collection(db, collection_id=card_id)
    if db_card is None:
        raise HTTPException(status_code=404, detail="Collection not found")
    return db_card
"""