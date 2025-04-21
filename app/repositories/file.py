from sqlalchemy import select
from typing import Type

from app.db import FileTable

from .base import BaseSQLAlchemyRepository, SchemaType


__all__ = ["FileRepository"]


class FileRepository(BaseSQLAlchemyRepository):
    table = FileTable

    async def get_by_id(self, file_id, output_schema: Type[SchemaType]) -> SchemaType | None:
        return await self.get_one_or_none(self._item_id_filter(file_id), output_schema)
    
    async def get_by_owner(self, owner_id: int, limit: int | None, offset: int) -> list[int]:
        query = select(self.table.c.id).where(self.table.c.owner_id == owner_id).offset(offset)
        if limit is not None:
            query = query.limit(limit)
        result = await self.connection.execute(query)
        return list(result.scalars().all())
    
    async def delete_by_id(self, file_id: int):
        await self.delete(self._item_id_filter(file_id))
