from sqlalchemy import and_, select, insert, update
from typing import Type

from app.db.models import CardCollectionTable, CollectionTable, CardTable
from app.schemas import Collection, Card

from .base import BaseSQLAlchemyRepository, SchemaType


__all__ = ["CardCollectionRepository"]


class CardCollectionRepository(BaseSQLAlchemyRepository):
    collection_table = CollectionTable
    card_table = CardTable
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
    
    async def __is_card_public_by_collections(self, card_id: int) -> bool:
        for collection in await self.get_card_collections(card_id, Collection):
            if collection.is_public:
                return True
        return False

    async def refresh_card_publicity(self, card_id: int) -> Card:
        is_public_new = await self.__is_card_public_by_collections(card_id)
        result = await self.connection.execute(
            update(self.card_table)
                .where(self.card_table.c.id == card_id)
                .values(is_public=is_public_new)
                .returning(self.card_table.c[*Card.fields()])
        )
        return Card(**result.mappings().first())
    
    async def update_cards_publicity(
            self, collection_id: int, is_public: bool
    ) -> list[Card]:
        if is_public:
            result = await self.connection.execute(
                update(self.card_table)
                    .where(self.card_table.c.id == self.table.c.card_id)
                    .where(self.table.c.collection_id == collection_id)
                    .values(is_public=True)
                    .returning(self.card_table.c[*Card.fields()])
            )
            return [Card(**elem) for elem in result.mappings().all()]
        else:
            return [
                await self.refresh_card_publicity(card_id)
                for card_id in await self.get_collection_cards(collection_id)
            ]
