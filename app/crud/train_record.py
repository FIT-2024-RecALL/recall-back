from sqlalchemy import select, insert, desc, text, func
from sqlalchemy.ext.asyncio import AsyncConnection

from app import TrainRecordTable
from app.helpers.training import compute_new_card_progress, compute_repeat_interval_duration
from app.schemas import TrainRecord, TrainRecordCreate

__all__ = [
    "get_train_records", "get_user_card_last_train_record", "create_train_record",
]


async def get_train_records(conn: AsyncConnection, limit: int | None, skip: int):
    query = select(TrainRecordTable.c[*TrainRecord.model_fields]).offset(skip)
    if limit is not None:
        query = query.limit(limit)
    return await conn.execute(query)


async def get_user_card_last_train_record(
        conn: AsyncConnection, user_id: int, card_id: int
) -> TrainRecord | None:
    query = (select(TrainRecordTable.c[*TrainRecord.model_fields])
             .where(TrainRecordTable.c.user_id == user_id,
                    TrainRecordTable.c.card_id == card_id)
             .order_by(desc(TrainRecordTable.c.id)).limit(1))
    result = (await conn.execute(query)).mappings().first()
    return result if result is None else TrainRecord(**result)


async def create_train_record(
        conn: AsyncConnection, card_id: int, user_id: int, prev_progress: float,
        train_data: TrainRecordCreate
) -> TrainRecord:
    repeat_date = func.now()
    progress = compute_new_card_progress(prev_progress, train_data.mark)
    repeat_interval = text(f"INTERVAL {compute_repeat_interval_duration(progress)} MINUTES")
    insert_query = insert(TrainRecordTable).values(
        card_id=card_id, user_id=user_id,
        progress=progress, **train_data.model_dump(),
        repeat_date=repeat_date, next_repeat_date=repeat_date+repeat_interval
    ).returning(TrainRecordTable.c[*TrainRecord.model_fields])
    result = (await conn.execute(insert_query)).mappings().first()  ## result не может быть None
    await conn.commit()
    return TrainRecord(**result)
