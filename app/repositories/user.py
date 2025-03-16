from sqlalchemy import select, and_, or_
from typing import Type

from app.db import UserTable

from .base import SchemaType, BaseSQLAlchemyRepository


__all__ = ["UserRepository"]


class UserRepository(BaseSQLAlchemyRepository):
    table = UserTable

    async def get_user_by_id(
            self, user_id: int, output_schema: Type[SchemaType]
    ) -> SchemaType | None:
        return await self.get_one_or_none(self.user_id_filter(user_id), output_schema)

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

    async def update_user_by_id(
            self, user_id: int, update_values: dict, output_schema: Type[SchemaType]
    ) -> SchemaType:
        return await self.update_one(self.user_id_filter(user_id), update_values, output_schema)

    async def delete_user_by_id(self, user_id) -> None:
        await self.delete(self.user_id_filter(user_id))

    async def exists_user_with_id(self, user_id: int) -> bool:
        return await self.exists(self.user_id_filter(user_id))

    def user_id_filter(self, user_id: int):
        return self.table.c.id == user_id

