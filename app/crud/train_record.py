from sqlalchemy import select, insert, desc
from sqlalchemy.ext.asyncio import AsyncConnection

from app import TrainRecordTable
from app.schemas import TrainRecord, TrainRecordCreate

__all__ = [
    "get_train_records", "get_user_card_last_train_record", "create_train_record",
]


async def get_train_records(conn: AsyncConnection, limit: int | None, skip: int):
    query = select(TrainRecordTable.c[*TrainRecord.model_fields]).offset(skip)
    if limit is not None:
        query = query.limit(limit)
    return await conn.execute(query)


async def get_user_card_last_train_record(conn: AsyncConnection, user_id: int, card_id: int):
    query = (select(TrainRecordTable.c[*TrainRecord.model_fields])
             .where(TrainRecordTable.c.user_id == user_id,
                    TrainRecordTable.c.card_id == card_id)
             .order_by(desc(TrainRecordTable.c.id)).limit(1))
    return await conn.execute(query)


async def create_train_record(
        conn: AsyncConnection, card_id: int, user_id: int,train_record: TrainRecordCreate
):
    insert_query = insert(TrainRecordTable).values(
        card_id=card_id, user_id=user_id, **train_record.model_dump()
    ).returning(TrainRecordTable.c[*TrainRecord.model_fields])
    result = await conn.execute(insert_query)
    await conn.commit()
    return result.mappings().first()
