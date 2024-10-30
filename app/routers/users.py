from fastapi import APIRouter, HTTPException
from sqlalchemy import select, exists, insert, or_

from app import schemas, models
from app.database import engine


router = APIRouter(
    prefix="/users",
    tags=["user"]
)

temp_hash = lambda x: x


@router.post("/", response_model=schemas.user.User)
def create_user(user: schemas.user.UserCreate):
    check_query = select(exists().where(or_(
        models.UserTable.c.email == user.email,
        models.UserTable.c.nickname == user.nickname
    )))
    insert_query = insert(models.UserTable).values(
        email=user.email,
        nickname=user.nickname,
        hashed_password=temp_hash(user.password)
    ).returning(models.UserTable.c["id", "email", "nickname"])
    with engine.connect() as conn:
        if conn.execute(check_query).scalar():
            raise HTTPException(status_code=400, detail="Email or Nickname already registered")
        result = conn.execute(insert_query).first()
        conn.commit()
        return schemas.user.User(
            id=result.id,
            email=result.email,
            nickname=result.nickname
        )


@router.get("/", response_model=list[schemas.user.User])
def read_users(skip: int = 0, limit: int = 100):
    query = select(models.UserTable).offset(skip).limit(limit)
    with engine.connect() as conn:
        result = conn.execute(query)
        return [schemas.user.User(id=row[0], email=row[1], nickname=row[2]) for row in result]


@router.get("/{user_id}", response_model=schemas.user.User)
def read_user(user_id: int):
    query = select(models.UserTable).where(models.UserTable.c.id == user_id)
    with engine.connect() as conn:
        user = conn.execute(query).first()
        return schemas.user.User(id=user[0], email=user[1], nickname=user[2])
