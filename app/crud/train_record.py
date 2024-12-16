from sqlalchemy import select, insert, desc, text, func
from sqlalchemy.ext.asyncio import AsyncConnection

from .card_collection import get_collection_cards
from app.models import TrainRecordTable
from app.helpers import compute_new_card_progress, compute_repeat_interval_duration
from app.schemas import TrainRecord, TrainRecordCreate

__all__ = [
    "get_train_records", "create_train_record", "get_training_cards",
    "get_user_card_last_train_record"
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
        conn: AsyncConnection, card_id: int, user_id: int,
        train_data: TrainRecordCreate, prev_progress: float
) -> TrainRecord:
    repeat_date = func.now()
    progress = compute_new_card_progress(prev_progress, train_data.mark)
    repeat_interval = text(f"INTERVAL '{compute_repeat_interval_duration(progress)} minutes'")
    insert_query = insert(TrainRecordTable).values(
        card_id=card_id, user_id=user_id,
        progress=progress, **train_data.model_dump(),
        repeat_date=repeat_date, next_repeat_date=repeat_date+repeat_interval
    ).returning(TrainRecordTable.c[*TrainRecord.model_fields])
    result = await conn.execute(insert_query)  ## result не может быть None
    await conn.commit()
    return TrainRecord(**result.mappings().first())


async def get_training_cards(conn: AsyncConnection, user_id: int, collection_id: int) -> list[int]:
    collection_card_ids: set[int] = set(await get_collection_cards(conn, collection_id))
    subquery = (
        select(TrainRecordTable.c.card_id, func.max(TrainRecordTable.c.id).label("last_id"))
        .where(TrainRecordTable.c.card_id.in_(collection_card_ids),
            TrainRecordTable.c.user_id == user_id)
        .group_by(TrainRecordTable.c.card_id)
        .subquery()
    )
    not_training_card_ids: set[int] = set((await conn.execute(
        select(TrainRecordTable.c.card_id)
        .join(subquery, TrainRecordTable.c.id == subquery.c.last_id)
        .where(TrainRecordTable.c.next_repeat_date > func.now())
    )).scalars().all())
    return list(collection_card_ids.difference(not_training_card_ids))
