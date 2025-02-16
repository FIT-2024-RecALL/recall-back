from abc import ABC, abstractmethod
from sqlalchemy import Table, insert, select, update, delete, exists
from sqlalchemy.ext.asyncio import AsyncConnection


__all__ = ["BaseRepository", "SQLAlchemyRepository"]


class BaseRepository(ABC):
    @abstractmethod
    async def create(self, input_data, output_fields):
        raise NotImplementedError

    @abstractmethod
    async def get_one_or_none(self, filter_data, filter_func, output_fields):
        raise NotImplementedError

    @abstractmethod
    async def get_all(self, output_fields, limit, offset):
        raise NotImplementedError

    @abstractmethod
    async def update_one(self, filter_data, filter_func, update_values, output_fields):
        raise NotImplementedError

    @abstractmethod
    async def delete(self, filter_data, filter_func):
        raise NotImplementedError

    @abstractmethod
    async def exists(self, filter_data, filter_func):
        raise NotImplementedError


class SQLAlchemyRepository(BaseRepository):
    table: Table = ...

    def __init__(self, conn: AsyncConnection):
        self.connection = conn

    async def create(self, input_data: dict, output_fields: list[str]) -> dict:
        result = await self.connection.execute(
            insert(self.table).values(**input_data).returning(self.table.c[*output_fields])
        )
        return dict(result.mappings().first())

    async def get_one_or_none(
            self, filter_data: dict, filter_func, output_fields: list[str]
    ) -> dict | None:
        result = (await self.connection.execute(
            select(self.table.c[*output_fields]).where(filter_func(filter_data))
        )).mappings().first()
        return result

    async def get_all(
            self, output_fields: list[str], limit: int, offset: int
    ) -> list[dict]:
        result = await self.connection.execute(
            select(self.table.c[*output_fields]).limit(limit).offset(offset)
        )
        return [*result.mappings().all()]

    async def update_one(
            self,
            filter_data: dict, filter_func,
            update_values: dict,
            output_fields: list[str]
    ) -> dict:
        result = await self.connection.execute(
            update(self.table).where(filter_func(filter_data)).values(**update_values)
            .returning(self.table.c[*output_fields])
        )
        return dict(result.mappings().first())

    async def delete(self, filter_data: dict, filter_func) -> None:
        await self.connection.execute(delete(self.table).where(filter_func(filter_data)))

    async def exists(self, filter_data: dict, filter_func) -> bool:
        result = await self.connection.execute(select(exists().where(filter_func(filter_data))))
        return result is not None
