from abc import ABC, abstractmethod
from pydantic import BaseModel
from sqlalchemy import Table, insert

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

    async def create(self, input_data: dict, output_schema: BaseModel):
        async with get_db_engine().begin() as conn:
            result = await conn.execute(
                insert(self.table).values(**input_data)
                .returning(self.table.c[*output_schema.model_fields])
            )
            return output_schema(**result.mappings().first())
