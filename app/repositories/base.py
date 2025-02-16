from abc import ABC, abstractmethod
from pydantic import BaseModel
from sqlalchemy import Table, insert, select
from sqlalchemy.ext.asyncio import AsyncConnection
from typing import Type, TypeVar


__all__ = ["BaseRepository", "SQLAlchemyRepository"]


SchemaType = TypeVar("SchemaType", bound=BaseModel)


class BaseRepository(ABC):
    @abstractmethod
    async def create(self, input_data, output_schema):
        raise NotImplementedError

    @abstractmethod
    async def get_one_or_none(self, filter_data, output_schema, need_all):
        raise NotImplementedError

    @abstractmethod
    async def get_all(self, output_schema, limit, offset):
        raise NotImplementedError

    @abstractmethod
    async def update(self):
        raise NotImplementedError

    @abstractmethod
    async def delete(self):
        raise NotImplementedError

    @abstractmethod
    async def exists(self):
        raise NotImplementedError


class SQLAlchemyRepository(BaseRepository):
    table: Table = ...

    def __init__(self, conn: AsyncConnection):
        self.connection = conn

    async def create(self, input_data: dict, output_schema: Type[SchemaType]) -> SchemaType:
        result = await self.connection.execute(
            insert(self.table).values(**input_data)
            .returning(self.table.c[*output_schema.model_fields])
        )
        return output_schema(**result.mappings().first())

    async def get_one_or_none(
            self, filter_data: dict, filter_func, output_schema: Type[SchemaType]
    ) -> SchemaType:
        result = await self.connection.execute(
            select(self.table.c[*output_schema.model_fields]).where(filter_func(filter_data))
        )
        return result.mappings().first() and output_schema(**result.mappings().first())

    async def get_all(
            self, output_schema: Type[SchemaType], limit: int, offset: int
    ) -> list[SchemaType]:
        result = await self.connection.execute(
            select(self.table.c[*output_schema.model_fields]).limit(limit).offset(offset)
        )
        return [output_schema(**elem) for elem in result.mappings().all()]




"""
class UserRepository(SQLAlchemyRepository):
    table = UserTable


class UserService:
    def __init__(self, user_repo: UserRepository):
        self.user_repo = user_repo

    async def create_user(self, user: UserCreate) -> User:
        input_data = user.model_dump()
        return await self.user_repo.create(input_data, User)    
"""
