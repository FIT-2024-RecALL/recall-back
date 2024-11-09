from sqlalchemy import select, insert
from sqlalchemy.ext.asyncio import AsyncConnection

from app.crud.card import check_card_id
from app.crud.user import check_user_id
from app.models import TrainRecordTable
from app.schemas.train_record import TrainRecord, TrainRecordCreate


async def get_train_record(conn: AsyncConnection, train_record_id: int):
    query = select(TrainRecordTable.c[*TrainRecord.model_fields]).where(
        TrainRecordTable.c.id == train_record_id
    )
    result = await conn.execute(query)
    return result.mappings().first()


async def get_train_records(conn: AsyncConnection, limit: int, skip: int):
    query = select(TrainRecordTable.c[*TrainRecord.model_fields]).limit(limit).offset(skip)
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


async def create_train_record(
        conn: AsyncConnection,
        card_id: int, user_id: int,
        train_record: TrainRecordCreate
):
    await check_card_id(conn, card_id)
    await check_user_id(conn, user_id)

    insert_query = insert(TrainRecordTable).values(
        card_id=card_id, user_id=user_id,
        **train_record.model_dump()
    ).returning(TrainRecordTable.c[*TrainRecord.model_fields])
    result = await conn.execute(insert_query)
    await conn.commit()
    return result.mappings().first()
