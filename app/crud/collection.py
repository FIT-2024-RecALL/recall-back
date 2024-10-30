from sqlalchemy import Connection, select, insert, exists, or_

from app import models, schemas


def get_collection(conn: Connection, collection_id: int):
    query = select(models.CollectionTable.c[*schemas.collection.Collection.model_fields]).where(
        models.CollectionTable.c.id == collection_id
    )
    return conn.execute(query).mappings().first()


def get_collections(conn: Connection, limit: int, skip: int):
    query = (select(models.CollectionTable.c[*schemas.collection.Collection.model_fields])
             .limit(limit)).offset(skip)
    return conn.execute(query).mappings().all()


def get_collection_cards():
    pass


def create_collection(
        conn: Connection, user_id: int, collection: schemas.collection.CollectionCreate
):
    check_user = select(exists().where(models.UserTable.c.id == user_id))  ## можно будет вынести в отдельный пользовательский crud
    if not conn.execute(check_user).scalar():
        raise ValueError("User not found")

    insert_query = (insert(models.CollectionTable).values(
        owner_id=user_id,
        **collection.model_dump()
    ).returning(models.CollectionTable.c[*schemas.collection.Collection.model_fields]))
    result = conn.execute(insert_query).mappings().first()
    conn.commit()
    return result
