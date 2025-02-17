from sqlalchemy import select, insert, exists, and_, or_, delete, update
from sqlalchemy.ext.asyncio import AsyncConnection
from typing import Type

from app.db.models import UserTable
from app.core import get_password_hash, verify_password
from app.schemas import User, UserAuth, UserBase, UserCreate

from .base import SchemaType, SQLAlchemyRepository


"""
class UserService:
    def __init__(self, user_repo: UserRepository):
        self.user_repo = user_repo

    async def create_user(self, user: UserCreate) -> User:
        input_data = user.model_dump()
        return await self.user_repo.create(input_data, User)
        

async def authenticate_user(conn: AsyncConnection, user_data: UserAuth) -> User:
    user = await get_user_by_email(conn, user_data.email)
    if user is None or not verify_password(user_data.password, user["hashed_password"]):
        raise ValueError("Entered email or password is not correct")
    return User(**user)  
"""


class UserRepository(SQLAlchemyRepository):
    table = UserTable

    async def get_user_by_column(self, column_value: dict, output_schema: Type[SchemaType]) -> SchemaType:
        column_filter = and_(self.table.c[key] == value for key, value in column_value.items())
        return await self.get_one_or_none(column_filter, output_schema)

"""
# UserDTO(**UserCreate().model_dump()).table_dict()["hashed_password"] = get_hash
async def create_user(conn: AsyncConnection, user: UserCreate) -> User:
    query = insert(UserTable).values(
        email=user.email, nickname=user.nickname, hashed_password=get_password_hash(user.password)
    ).returning(UserTable.c[*User.model_fields])
    result = await conn.execute(query)
    await conn.commit()
    return User(**result.mappings().first())

# UserDTO
async def get_user_by_email(conn: AsyncConnection, email: str):
    result = await conn.execute(select(UserTable).where(UserTable.c.email == email))
    return result.mappings().first()

# User
async def get_user(conn: AsyncConnection, user_id: int) -> User | None:
    result = (await conn.execute(
        select(UserTable.c[*User.model_fields]).where(UserTable.c.id == user_id)
    )).mappings().first()
    return result if result is None else User(**result)
"""

async def update_user(conn: AsyncConnection, user_id: int, user: UserBase) -> User:
    query = (update(UserTable).where(UserTable.c.id == user_id).values(**user.model_dump())
             .returning(UserTable.c[*User.model_fields]))
    result = await conn.execute(query)
    await conn.commit()
    return User(**result.mappings().first())


async def delete_user(conn: AsyncConnection, user_id: int) -> None:
    await conn.execute(delete(UserTable).where(UserTable.c.id == user_id))
    await conn.commit()


async def check_user_id(conn: AsyncConnection, user_id: int) -> None:
    result = await conn.execute(select(exists().where(UserTable.c.id == user_id)))
    if not result.scalar():
        raise ValueError("User not found")


async def find_users_by_data(conn: AsyncConnection, user: UserBase) -> list[int]:
    return list((await conn.execute(select(UserTable.c.id).where(
        or_(UserTable.c.email == user.email, UserTable.c.nickname == user.nickname)
    ))).scalars().all())

