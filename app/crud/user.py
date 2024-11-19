from jose import jwt, JWTError
from sqlalchemy import select, insert, exists, or_
from sqlalchemy.ext.asyncio import AsyncConnection

from app.auth.utils import settings, get_password_hash, verify_password
from app.models import UserTable
from app.schemas.user import User, UserAuth, UserCreate


async def get_user(conn: AsyncConnection, user_id: int):
    query = select(UserTable.c[*User.model_fields]).where(UserTable.c.id == user_id)
    result = await conn.execute(query)
    return result.mappings().first()


async def get_users(conn: AsyncConnection, *, limit: int, skip: int):
    query = select(UserTable.c[*User.model_fields]).limit(limit).offset(skip)
    result = await conn.execute(query)
    return result.mappings().all()


async def check_user_id(conn: AsyncConnection, user_id: int):
    query = select(exists().where(UserTable.c.id == user_id))
    result = await conn.execute(query)
    if not result.scalar():
        raise ValueError("User with this id doesn't exist")


async def check_user_data(conn: AsyncConnection, user: UserCreate):
    query = select(exists().where(or_(
        UserTable.c.email == user.email,
        UserTable.c.nickname == user.nickname
    )))
    result = await conn.execute(query)
    if result.scalar():
        raise ValueError("Email or Nickname already registered")


async def create_user(conn: AsyncConnection, user: UserCreate):
    await check_user_data(conn, user)
    query = insert(UserTable).values(
        email=user.email,
        nickname=user.nickname,
        hashed_password=get_password_hash(user.password)
    ).returning(UserTable.c[*User.model_fields])

    result = await conn.execute(query)
    await conn.commit()
    return result.mappings().first()


async def get_user_via_email(conn: AsyncConnection, email: str):
    query = select(UserTable).where(UserTable.c.email == email)
    result = await conn.execute(query)
    return result.mappings().first()


async def authenticate_user(conn: AsyncConnection, user_data: UserAuth) -> int:
    user = await get_user_via_email(conn, user_data.email)
    if user is None or not verify_password(user_data.password, user["hashed_password"]):
        raise ValueError("Entered email or password is incorrect")
    return user["id"]


def get_profile_id(token: str) -> int:
    try:
        auth_data = settings.auth_data
        payload = jwt.decode(token, auth_data['secret_key'], algorithms=[auth_data['algorithm']])
    except JWTError:
        raise ValueError("Invalid or expired token")

    user_id = payload.get('sub')
    if not user_id:
        raise ValueError("User ID is undefined")
    return int(user_id)
