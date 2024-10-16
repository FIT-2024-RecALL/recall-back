from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import crud, schemas
from app.database import get_db


router = APIRouter(
    prefix="/train_records",
    tags=["train_record"]
)


@router.get("/", response_model=list[schemas.train_record.TrainRecord])
def read_train_records(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    train_records = crud.train_record.get_train_records(db, skip=skip, limit=limit)
    return train_records


@router.get("/{train_record_id}", response_model=schemas.train_record.TrainRecord)
def read_train_record(train_record_id: int, db: Session = Depends(get_db)):
    db_train_record = crud.train_record.get_train_record(db, train_record_id=train_record_id)
    if db_train_record is None:
        raise HTTPException(status_code=404, detail="TrainRecord not found")
    return db_train_record
