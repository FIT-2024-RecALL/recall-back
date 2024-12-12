from datetime import datetime, timedelta, timezone

from sqlalchemy import select, insert, desc
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


## TODO: В БУДУЮЩЕМ ВЫЧИСЛЯТЬ ДАТУ НА СТОРОНЕ БАЗЫ ДАННЫХ
async def create_train_record(
        conn: AsyncConnection, card_id: int, user_id: int, train_data: TrainRecordCreate, prev_progress: float
):
    repeat_date: datetime = datetime.now(timezone.utc)
    progress: float = compute_new_card_progress(prev_progress, train_data.mark)
    interval_minutes_duration: int = compute_repeat_interval_duration(progress)
    next_repeat_date: datetime = repeat_date + timedelta(minutes=interval_minutes_duration)
    insert_query = insert(TrainRecordTable).values(
        card_id=card_id, user_id=user_id, **train_data.model_dump(),
        repeat_date=repeat_date, next_repeat_date=next_repeat_date, progress=progress
    ).returning(TrainRecordTable.c[*TrainRecord.model_fields])
    result = await conn.execute(insert_query)
    await conn.commit()
    return result.mappings().first()
