from fastapi import APIRouter, HTTPException

from app import crud
from app.dependencies import DBConnection, JWToken
from app.schemas.train_record import TrainRecord, TrainRecordCreate


router = APIRouter(
    prefix="/train_records",
    tags=["train_record"]
)


@router.get("/admin/{train_record_id}", response_model=TrainRecord)
async def read_train_record(conn: DBConnection, train_record_id: int):
    db_train_record = await crud.train_record.get_train_record(conn, train_record_id)
    if db_train_record is None:
        raise HTTPException(status_code=404, detail="TrainRecord not found")
    return db_train_record


@router.get("/admin", response_model=list[TrainRecord])
async def read_train_records(conn: DBConnection, limit: int = 100, skip: int = 0):
    return await crud.train_record.get_train_records(conn, skip=skip, limit=limit)


@router.get("/", response_model=list[TrainRecord])
async def read_user_train_records(conn: DBConnection, token: JWToken):
    pass


@router.post("/{card_id}", response_model=TrainRecord)
async def create_train_record_for_user(
        conn: DBConnection, token: JWToken, card_id: int, train_record: TrainRecordCreate
):
    try:
        user_id: int = await crud.user.get_profile_id(conn, token)
        return await crud.train_record.create_train_record(conn, card_id, user_id, train_record)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/{card_id}", response_model=list[TrainRecord])
async def read_user_card_train_records(conn: DBConnection, token: JWToken, card_id: int):
    pass
