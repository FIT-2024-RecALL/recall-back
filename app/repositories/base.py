from abc import ABC, abstractmethod
from pydantic import BaseModel
from sqlalchemy import Table, insert
from typing import Type

from app.core import SchemaType
from app.db import get_db_engine


class BaseRepository(ABC):
    @abstractmethod
    async def create(self, input_data: dict, output_schema: BaseModel):
        raise NotImplementedError

    @abstractmethod
    async def get_by_id(self):
        raise NotImplementedError

    @abstractmethod
    async def get_all(self):
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

    async def create(self, input_data: dict, output_schema: Type[SchemaType]) -> SchemaType:
        async with get_db_engine().begin() as conn:
            result = await conn.execute(
                insert(self.table).values(**input_data)
                .returning(self.table.c[*output_schema.model_fields])
            )
            return output_schema(**result.mappings().first())


    async def get_by_id(self):



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