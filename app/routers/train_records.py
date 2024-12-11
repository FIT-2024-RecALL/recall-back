from fastapi import APIRouter, HTTPException

from app import crud
from app.helpers import DBConnection, UserID
from app.schemas import TrainRecord, TrainRecordCreate


router = APIRouter(
    prefix="/train_records",
    tags=["train_record"]
)


@router.post("/{card_id}", response_model=TrainRecord)
async def create_train_record(
        conn: DBConnection, user_id: UserID, card_id: int, train_record: TrainRecordCreate
):
    try:
        await crud.check_user_id(conn, user_id)
        await crud.check_card_id(conn, user_id, card_id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    return await crud.create_train_record(conn, card_id, user_id, train_record)


@router.get("/{card_id}", response_model=list[TrainRecord])
async def read_card_last_train_record(conn: DBConnection, user_id: UserID, card_id: int):
    try:
        await crud.check_user_id(conn, user_id)
        await crud.check_card_id(conn, user_id, card_id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    return await crud.get_user_card_last_train_record(conn, user_id, card_id)
