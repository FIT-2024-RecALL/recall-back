from sqlalchemy import and_, select, insert
from typing import Type

from app.db.models import CardCollectionTable, CollectionTable

from .base import BaseSQLAlchemyRepository, SchemaType


__all__ = ["CardCollectionRepository"]


class CardCollectionRepository(BaseSQLAlchemyRepository):
    collection_table = CollectionTable
    table = CardCollectionTable

    async def set_card_collection_connections(
            self, card_id: int, collections: list[int]
    ) -> None:
        await self.connection.execute(
            insert(self.table),
            [{"card_id": card_id, "collection_id": collection} for collection in collections],
        )

    async def unset_card_collection_connections(
            self, card_id: int, collections: list[int]
    ) -> None:
       await self.delete(
           and_(self.table.c.card_id == card_id, self.table.c.collection_id.in_(collections))
       )

    async def fetch_card_collections(self, card_id: int) -> list[int]:
        result = await self.connection.execute(
            select(self.table.c.collection_id).where(self.table.c.card_id == card_id)
        )
        return list(result.scalars().all())

    async def filter_cards_with_collection(self, cards: set[int]) -> set[int]:
        """
        Фильтрует исходное множество идентификаторов карт, оставляя только те,
        которые имеют связь хотя бы с одной коллекцией в таблице CardCollectionTable.
        """
        result = await self.connection.execute(
            select(self.table.c.card_id).where(self.table.c.card_id.in_(cards))
        )
        return set(result.scalars().all())

    async def filter_owner_exist_collections(
            self, owner_id: int, collections: list[int]
    ) -> list[int]:
        result = await self.connection.execute(
            select(self.collection_table.c.id).where(and_(
                self.collection_table.c.id.in_(set(collections)),
                self.collection_table.c.owner_id == owner_id
            ))
        )
        return list(result.scalars().all())

    async def get_collection_cards(self, collection_id: int) -> list[int]:
        result = await self.connection.execute(
            select(self.table.c.card_id).where(self.table.c.collection_id == collection_id)
        )
        return list(result.scalars().all())

    async def get_card_collections(
            self, card_id: int, output_schema: Type[SchemaType]
    ) -> list[SchemaType]:
        result = await self.connection.execute(
            select(self.collection_table.c[*output_schema.fields()])
            .join(self.table, self.collection_table.c.id == self.table.c.collection_id)
            .where(self.table.c.card_id == card_id)
        )
        return [output_schema(**elem) for elem in result.mappings().all()]
