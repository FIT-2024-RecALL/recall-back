from fastapi import APIRouter, HTTPException

from app import crud, DBConnection, UserID
from app.schemas import TrainRecord, TrainRecordCreate


router = APIRouter(
    prefix="/train_records",
    tags=["train_record"]
)


@router.get("/admin/{train_record_id}", response_model=TrainRecord)
async def read_train_record(conn: DBConnection, train_record_id: int):
    db_train_record = await crud.get_train_record(conn, train_record_id)
    if db_train_record is None:
        raise HTTPException(status_code=404, detail="TrainRecord not found")
    return db_train_record


@router.get("/admin", response_model=list[TrainRecord])
async def read_train_records(conn: DBConnection, skip: int = 0, limit: int | None = None):
    return await crud.get_train_records(conn, skip=skip, limit=limit)


@router.get("/", response_model=list[TrainRecord])
async def read_user_train_records(conn: DBConnection, user_id: UserID):
    try:
        return await crud.get_user_train_records(conn, user_id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/{card_id}", response_model=TrainRecord)
async def create_train_record_for_user(
        conn: DBConnection, user_id: UserID, card_id: int, train_record: TrainRecordCreate
):
    try:
        await crud.check_card_id(conn, card_id)
        await crud.check_user_id(conn, user_id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    return await crud.create_train_record(conn, card_id, user_id, train_record)


@router.get("/{card_id}", response_model=list[TrainRecord])
async def read_user_card_train_records(conn: DBConnection, user_id: UserID, card_id: int):
    try:
        await crud.check_card_id(conn, card_id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    return await crud.get_user_card_train_records(conn, user_id, card_id)


@router.get("/record/{card_id}", response_model=list[TrainRecord])
async def read_user_card_last_train_record(conn: DBConnection, user_id: UserID, card_id: int):
    try:
        await crud.check_card_id(conn, card_id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    return await crud.get_user_card_last_train_record(conn, user_id, card_id)
