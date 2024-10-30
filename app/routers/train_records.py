"""from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import crud, schemas
from app.database import get_db


router = APIRouter(
    prefix="/train_records",
    tags=["train_record"]
)


@router.post("/{card_id}/{user_id}", response_model=schemas.train_record.TrainRecord)
def create_train_record_for_user(
        card_id: int, user_id: int, train_record: schemas.train_record.TrainRecordCreate, db: Session = Depends(get_db)
):
    db_user = crud.user.get_user(db, user_id)
    db_card = crud.card.get_card(db, card_id)
    if not db_user or not db_card:
        raise HTTPException(status_code=400, detail="User or Card with this id doesn't exist")
    return crud.train_record.create_train_record(db=db, train_record=train_record, card_id=card_id, user_id=user_id)


@router.get("/", response_model=list[schemas.train_record.TrainRecord])
def read_train_records(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.train_record.get_train_records(db, skip=skip, limit=limit)


@router.get("/{train_record_id}", response_model=schemas.train_record.TrainRecord)
def read_train_record(train_record_id: int, db: Session = Depends(get_db)):
    db_train_record = crud.train_record.get_train_record(db, train_record_id=train_record_id)
    if db_train_record is None:
        raise HTTPException(status_code=404, detail="TrainRecord not found")
    return db_train_record
"""