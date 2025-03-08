from sqlalchemy import select, and_, or_
from typing import Type

from app.db import UserTable

from .base import SchemaType, SQLAlchemyRepository


__all__ = ["UserRepository"]


class UserRepository(SQLAlchemyRepository):
    table = UserTable

    async def get_user_by_columns(
            self, column_values: dict, output_schema: Type[SchemaType]
    ) -> SchemaType | None:
        columns_filter = and_(self.table.c[key] == value for key, value in column_values.items())
        return await self.get_one_or_none(columns_filter, output_schema)

    async def find_users_by_creds(self, filter_data: dict) -> list[int]:
        result = await self.connection.execute(
            select(self.table.c.id).where(or_(
                self.table.c.email == filter_data["email"],
                self.table.c.nickname == filter_data["nickname"]
            ))
        )
        return list(result.scalars().all())
