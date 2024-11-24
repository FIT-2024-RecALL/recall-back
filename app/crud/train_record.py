from sqlalchemy import select, insert, desc, delete
from sqlalchemy.ext.asyncio import AsyncConnection

from app import TrainRecordTable
from app.crud import check_card_id, check_user_id
from app.schemas import TrainRecord, TrainRecordCreate

__all__ = [
    "get_user_card_train_records", "get_train_record", "get_train_records",
    "get_user_card_last_train_record", "get_user_train_records", "create_train_record",
    "delete_train_record_by_card"
]


async def get_train_record(conn: AsyncConnection, train_record_id: int):
    query = select(TrainRecordTable.c[*TrainRecord.model_fields]).where(
        TrainRecordTable.c.id == train_record_id
    )
    result = await conn.execute(query)
    return result.mappings().first()


async def get_train_records(conn: AsyncConnection, limit: int | None, skip: int):
    query = select(TrainRecordTable.c[*TrainRecord.model_fields]).offset(skip)
    if limit is not None:
        query = query.limit(limit)
    return await conn.execute(query)


async def get_user_train_records(conn: AsyncConnection, user_id: int):
    query = (select(TrainRecordTable.c[*TrainRecord.model_fields])
             .where(TrainRecordTable.c.user_id == user_id))
    return await conn.execute(query)


async def get_user_card_train_records(conn: AsyncConnection, user_id: int, card_id: int):
    ## card exist?
    query = (select(TrainRecordTable.c[*TrainRecord.model_fields])
             .where(TrainRecordTable.c.user_id == user_id,
                    TrainRecordTable.c.card_id == card_id))
    return await conn.execute(query)


async def get_user_card_last_train_record(conn: AsyncConnection, user_id: int, card_id: int):
    ## card exist?
    query = (select(TrainRecordTable.c[*TrainRecord.model_fields])
             .where(TrainRecordTable.c.user_id == user_id,
                    TrainRecordTable.c.card_id == card_id)
             .order_by(desc(TrainRecordTable.c.id)).limit(1))
    return await conn.execute(query)


async def create_train_record(
        conn: AsyncConnection,
        card_id: int, user_id: int,
        train_record: TrainRecordCreate
):
    await check_card_id(conn, card_id) ## Может вынести это в route?
    await check_user_id(conn, user_id) ## Может вынести это в route?

    insert_query = insert(TrainRecordTable).values(
        card_id=card_id, user_id=user_id,
        **train_record.model_dump()
    ).returning(TrainRecordTable.c[*TrainRecord.model_fields])
    result = await conn.execute(insert_query)
    await conn.commit()
    return result.mappings().first()


async def delete_train_record_by_card(conn: AsyncConnection, card_id: int):
    query = delete(TrainRecordTable).where(TrainRecordTable.c.card_id == card_id)
    await conn.execute(query)
    await conn.commit()
