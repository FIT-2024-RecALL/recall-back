from sqlalchemy import select, insert, exists, or_, delete, update
from sqlalchemy.ext.asyncio import AsyncConnection

from app import UserTable, get_password_hash, verify_password
from app.schemas import User, UserAuth, UserBase, UserCreate

__all__ = [
    "get_user", "get_users", "check_user_id", "find_users_by_data", "create_user",
    "get_user_via_email", "authenticate_user", "delete_user", "update_user"
]


async def get_user(conn: AsyncConnection, user_id: int) -> User | None:
    result = (await conn.execute(
        select(UserTable.c[*User.model_fields]).where(UserTable.c.id == user_id)
    )).mappings().first()
    return result if result is None else User(**result)


async def get_users(conn: AsyncConnection, *, limit: int, skip: int):
    result = await conn.execute(
        select(UserTable.c[*User.model_fields]).limit(limit).offset(skip)
    )
    return result.mappings().all()


async def check_user_id(conn: AsyncConnection, user_id: int) -> None:
    result = await conn.execute(select(exists().where(UserTable.c.id == user_id)))
    if not result.scalar():
        raise ValueError("User not found")


async def find_users_by_data(conn: AsyncConnection, user: UserBase) -> list[int]:
    return list((await conn.execute(select(UserTable.c.id).where(
        or_(UserTable.c.email == user.email, UserTable.c.nickname == user.nickname)
    ))).scalars().all())


async def create_user(conn: AsyncConnection, user: UserCreate) -> User:
    query = insert(UserTable).values(
        email=user.email, nickname=user.nickname, hashed_password=get_password_hash(user.password)
    ).returning(UserTable.c[*User.model_fields])

    result = await conn.execute(query)
    await conn.commit()
    return User(**result.mappings().first())


async def delete_user(conn: AsyncConnection, user_id: int) -> None:
    await conn.execute(delete(UserTable).where(UserTable.c.id == user_id))
    await conn.commit()


async def update_user(conn: AsyncConnection, user_id: int, user: UserBase) -> User:
    query = update(UserTable).where(UserTable.c.id == user_id).values(
        email=user.email, nickname=user.nickname
    ).returning(UserTable.c[*User.model_fields])

    result = await conn.execute(query)
    await conn.commit()
    return User(**result.mappings().first())


async def get_user_via_email(conn: AsyncConnection, email: str):
    result = await conn.execute(select(UserTable).where(UserTable.c.email == email))
    return result.mappings().first()


async def authenticate_user(conn: AsyncConnection, user_data: UserAuth) -> User:
    user = await get_user_via_email(conn, user_data.email)
    if user is None or not verify_password(user_data.password, user["hashed_password"]):
        raise ValueError("Entered email or password is not correct")
    return User(**user)
