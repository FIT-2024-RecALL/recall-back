from sqlalchemy import Connection, select, insert, exists, or_

from app import models, schemas


def get_user(conn: Connection, user_id: int):
    query = select(models.UserTable.c[*schemas.user.User.model_fields]).where(
        models.UserTable.c.id == user_id
    )
    return conn.execute(query).mappings().first()


def get_users(conn: Connection, *, limit: int, skip: int):
    query = select(models.UserTable.c[*schemas.user.User.model_fields]).limit(limit).offset(skip)
    return conn.execute(query).mappings().all()


temp_hash = lambda x: x

def create_user(conn: Connection, user: schemas.user.UserCreate):
    check_query = select(exists().where(or_(
        models.UserTable.c.email == user.email,
        models.UserTable.c.nickname == user.nickname
    )))
    if conn.execute(check_query).scalar():
        raise ValueError("Email or Nickname already registered")

    insert_query = insert(models.UserTable).values(
        email=user.email,
        nickname=user.nickname,
        hashed_password=temp_hash(user.password)
    ).returning(models.UserTable.c[*schemas.user.User.model_fields])

    result = conn.execute(insert_query).mappings().first()
    conn.commit()
    return result


def get_profile(conn: Connection):
    pass
