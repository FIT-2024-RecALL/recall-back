from fastapi import APIRouter, HTTPException

from app import crud, schemas
from app.dependencies import DBConnection


router = APIRouter(
    prefix="/train_records",
    tags=["train_record"]
)


@router.get("/{train_record_id}", response_model=schemas.train_record.TrainRecord)
def read_train_record(conn: DBConnection, train_record_id: int):
    db_train_record = crud.train_record.get_train_record(conn, train_record_id)
    if db_train_record is None:
        raise HTTPException(status_code=404, detail="TrainRecord not found")
    return db_train_record


@router.get("/", response_model=list[schemas.train_record.TrainRecord])
def read_train_records(conn: DBConnection, limit: int = 100, skip: int = 0):
    return crud.train_record.get_train_records(conn, skip=skip, limit=limit)


@router.post("/{card_id}/{user_id}", response_model=schemas.train_record.TrainRecord)
def create_train_record_for_user(
        conn: DBConnection, card_id: int, user_id: int, train_record: schemas.train_record.TrainRecordCreate
):
    try:
        created_train_record = crud.train_record.create_train_record(conn, card_id, user_id, train_record)
        return created_train_record
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
