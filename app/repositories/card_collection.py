from sqlalchemy import and_, select, insert
from typing import Type

from app.db.models import CardCollectionTable, CollectionTable

from .base import BaseSQLAlchemyRepository, SchemaType


__all__ = ["CardCollectionRepository"]


"""
## CARD SERVICE
async def create_card_collection_connections(
        conn: AsyncConnection, user_id: int, card_id: int, collections: list[int]
) -> None:
    new_collections = await fetch_exist_owner_collections(conn, user_id, collections)
    if not new_collections:
        raise ValueError("Collections not found")
    await set_card_collection_connections(conn, card_id, new_collections)


## CARD SERVICE
async def update_card_collection_connections(
        conn: AsyncConnection, user_id: int, card_id: int, collections: list[int]
) -> None:
    request_collections: set[int] = set(await fetch_exist_owner_collections(conn, user_id, collections))
    if not request_collections:
        raise ValueError("Collections not found")
    old_collections: set[int] = set(await fetch_card_collections(conn, card_id))
    delete_collections: list[int] = list(old_collections.difference(request_collections))
    new_collections: list[int] = list(request_collections.difference(old_collections))
    if delete_collections:
        await unset_card_collection_connections(conn, card_id, delete_collections)
    if new_collections:
        await set_card_collection_connections(conn, card_id, new_collections)
"""


class CardCollectionRepository(BaseSQLAlchemyRepository):
    collection_table = CollectionTable
    table = CardCollectionTable

    async def set_card_collection_connections(self, card_id: int, collections: list[int]) -> None:
        await self.connection.execute(
            insert(self.table),
            [{"card_id": card_id, "collection_id": collection} for collection in collections],
        )

    async def get_collection_cards(self, collection_id: int) -> list[int]:
        result = await self.connection.execute(
            select(self.table.c.card_id).where(self.table.c.collection_id == collection_id)
        )
        return list(result.scalars().all())

    async def get_owner_card_collections(
            self, owner_id: int, card_id: int, output_schema: Type[SchemaType]
    ) -> list[SchemaType]:
        """
        Запрос такой сложный, потому что на данный момент мы исходим из предположения,
        что одна карточка может принадлежать разным пользователям.
        """
        result = await self.connection.execute(
            select(self.collection_table.c[*output_schema.fields()])
            .join(self.table, self.collection_table.c.id == self.table.c.collection_id)
            .where(self.collection_table.c.owner_id == owner_id, self.table.c.card_id == card_id)
        )
        return [output_schema(**elem) for elem in result.mappings().all()]

    async def fetch_card_collections(self, card_id: int) -> list[int]:
        result = await self.connection.execute(
            select(self.table.c.collection_id).where(self.table.c.card_id == card_id)
        )
        return list(result.scalars().all())

    async def fetch_exist_owner_collections(
            self, owner_id: int, collections_id: list[int]
    ) -> list[int]:
        exist_unique_collections = await self.connection.execute(
            select(self.collection_table.c.id).where(and_(
                self.collection_table.c.id.in_(set(collections_id)),
                self.collection_table.c.owner_id == owner_id
            ))
        )
        return list(exist_unique_collections.scalars().all())


    async def unset_card_collection_connections(self, card_id: int, collections: list[int]) -> None:
       await self.delete(
           and_(self.table.c.card_id == card_id, self.table.c.collection_id.in_(collections))
       )

    async def filter_cards_with_collection(self, cards: set[int]) -> set[int]:
        """
        Фильтрует исходное множество идентификаторов карт, оставляя только те,
        которые имеют связь хотя бы с одной коллекцией в таблице CardCollectionTable.
        """
        result = await self.connection.execute(
            select(self.table.c.card_id).where(self.table.c.card_id.in_(cards))
        )
        return set(result.scalars().all())
