from sqlalchemy import select, and_, or_
from typing import Type

from app.db import UserTable

from .base import SchemaType, SQLAlchemyRepository


__all__ = ["UserRepository"]


class UserRepository(SQLAlchemyRepository):
    table = UserTable

    async def get_user_by_columns(
            self, column_values: dict, output_schema: Type[SchemaType]
    ) -> SchemaType:
        columns_filter = and_(self.table.c[key] == value for key, value in column_values.items())
        return await self.get_one_or_none(columns_filter, output_schema)

    async def find_users_by_data(self, filter_data: dict) -> list[int]:
        result = await self.connection.execute(
            select(self.table.c.id).where(or_(
                self.table.c.email == filter_data["email"],
                self.table.c.nickname == filter_data["nickname"]
            ))
        )
        return list(result.scalars().all())

"""
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

# User
async def update_user(conn: AsyncConnection, user_id: int, user: UserBase) -> User:
    query = (update(UserTable).where(UserTable.c.id == user_id).values(**user.model_dump())
             .returning(UserTable.c[*User.model_fields]))
    result = await conn.execute(query)
    await conn.commit()
    return User(**result.mappings().first())
    
# nothing
async def delete_user(conn: AsyncConnection, user_id: int) -> None:
    await conn.execute(delete(UserTable).where(UserTable.c.id == user_id))
    await conn.commit()

# nothing
async def check_user_id(conn: AsyncConnection, user_id: int) -> None:
    result = await conn.execute(select(exists().where(UserTable.c.id == user_id)))
    if not result.scalar():
        raise ValueError("User not found")
"""
