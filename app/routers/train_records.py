from fastapi import APIRouter, HTTPException

from app import crud
from app.dependencies import DBConnection
from app.schemas.train_record import TrainRecord, TrainRecordCreate


router = APIRouter(
    prefix="/train_records",
    tags=["train_record"]
)


@router.get("/{train_record_id}", response_model=TrainRecord)
async def read_train_record(conn: DBConnection, train_record_id: int):
    db_train_record = await crud.train_record.get_train_record(conn, train_record_id)
    if db_train_record is None:
        raise HTTPException(status_code=404, detail="TrainRecord not found")
    return db_train_record


@router.get("/", response_model=list[TrainRecord])
async def read_train_records(conn: DBConnection, limit: int = 100, skip: int = 0):
    return await crud.train_record.get_train_records(conn, skip=skip, limit=limit)


@router.post("/{card_id}/{user_id}", response_model=TrainRecord)
async def create_train_record_for_user(
        conn: DBConnection, card_id: int, user_id: int, train_record: TrainRecordCreate
):
    try:
        return await crud.train_record.create_train_record(conn, card_id, user_id, train_record)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
