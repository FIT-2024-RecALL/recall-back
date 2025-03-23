from sqlalchemy import and_, select
from typing import Type

from app.db import CollectionTable

from .base import BaseSQLAlchemyRepository, SchemaType


__all__ = ["CollectionRepository"]


class CollectionRepository(BaseSQLAlchemyRepository):
    table = CollectionTable

    async def get_collection_by_id(
            self, collection_id: int, output_schema: Type[SchemaType]
    ) -> SchemaType | None:
        return await self.get_one_or_none(self._item_id_filter(collection_id), output_schema)

    async def get_owner_collections(
            self, owner_id: int, limit: int | None, offset: int, output_schema: Type[SchemaType]
    ) -> list[SchemaType]:
        query = (select(self.table.c[*output_schema.fields()])
                 .where(self.table.c.owner_id == owner_id).offset(offset))
        if limit is not None:
            query = query.limit(limit)
        result = await self.connection.execute(query)
        return [output_schema(**elem) for elem in result.mappings().all()]

    async def update_collection_by_id(
            self, collection_id: int, update_values: dict, output_schema: Type[SchemaType]
    ) -> SchemaType:
        return await self.update_one(
            self._item_id_filter(collection_id), update_values, output_schema
        )

    async def delete_collection(self, collection_id: int) -> None:
        await self.delete(self._item_id_filter(collection_id))

    async def exists_collection_with_owner(self, owner_id: int, collection_id: int) -> bool:
        return await self.exists(
            and_(self.table.c.owner_id == owner_id, self._item_id_filter(collection_id))
        )

    async def exists_collection_with_id(self, collection_id: int) -> bool:
        return await self.exists(self._item_id_filter(collection_id))
