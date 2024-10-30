from sqlalchemy import Connection, exists, select, insert

from app import models, schemas


def get_train_record(conn: Connection, train_record_id: int):
    query = select(models.TrainRecordTable.c[*schemas.train_record.TrainRecord.model_fields]).where(
        models.TrainRecordTable.c.id == train_record_id
    )
    return conn.execute(query).mappings().first()


def get_train_records(conn: Connection, limit: int, skip: int):
    query = (select(models.TrainRecordTable.c[*schemas.train_record.TrainRecord.model_fields])
             .limit(limit)).offset(skip)
    return conn.execute(query)


def create_train_record(
        conn: Connection,
        card_id: int, user_id: int,
        train_record: schemas.train_record.TrainRecordCreate
):
    check_card = select(exists().where(models.CardTable.c.id == card_id))
    if not conn.execute(check_card).scalar():
        raise ValueError("Card with this id doesn't exist")

    check_user = select(exists().where(models.UserTable.c.id == user_id))  ## можно будет вынести в отдельный пользовательский crud
    if not conn.execute(check_user).scalar():
        raise ValueError("User with this id doesn't exist")

    insert_query = insert(models.TrainRecordTable).values(
        card_id=card_id, user_id=user_id,
        **train_record.model_dump()
    ).returning(models.TrainRecordTable.c[*schemas.train_record.TrainRecord.model_fields])
    result = conn.execute(insert_query).mappings().first()
    conn.commit()
    return result
