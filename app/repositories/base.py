from abc import ABC, abstractmethod
from pydantic import BaseModel
from sqlalchemy import Table, insert
from sqlalchemy.ext.asyncio import AsyncConnection
from typing import Type, TypeVar


__all__ = ["BaseRepository", "SQLAlchemyRepository"]


SchemaType = TypeVar("SchemaType", bound=BaseModel)


class BaseRepository(ABC):
    @abstractmethod
    async def create(self, input_data, output_schema):
        raise NotImplementedError

    @abstractmethod
    async def get_by_id(self):
        raise NotImplementedError

    @abstractmethod
    async def get_all(self):
        raise NotImplementedError

    @abstractmethod
    async def update_by_id(self):
        raise NotImplementedError

    @abstractmethod
    async def delete_by_id(self):
        raise NotImplementedError

    @abstractmethod
    async def exists_by_id(self):
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
