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

    async def fetch_exist_owner_collections(
            self, owner_id: int, collections_id: list[int]
    ) -> list[int]:
        exist_unique_collections = await self.connection.execute(
            select(self.table.c.id).where(and_(
                self.table.c.id.in_(set(collections_id)), self.table.c.owner_id == owner_id
            ))
        )
        return list(exist_unique_collections.scalars().all())

    async def update_collection_by_id(
            self, collection_id: int, update_values: dict, output_schema: Type[SchemaType]
    ) -> SchemaType:
        return await self.update_one(
            self._item_id_filter(collection_id), update_values, output_schema
        )

    async def exists_collection_with_owner(self, owner_id: int, collection_id: int) -> bool:
        return await self.exists(
            and_(self.table.c.owner_id == owner_id, self._item_id_filter(collection_id))
        )

    async def exists_collection_with_id(self, collection_id: int) -> bool:
        return await self.exists(self._item_id_filter(collection_id))


"""

"""


async def _filter_connected_cards(conn: AsyncConnection, cards: set[int]) -> set[int]:
    # Фильтрует исходное множество идентификаторов карт, оставляя только те,
    # которые имеют связь хотя бы с одной коллекцией в таблице CardCollectionTable.
    # :param conn: Асинхронное соединение с базой данных.
    # :param cards: Исходное множество идентификаторов карт.
    # :return: Множество идентификаторов карт, которые имеют связь хотя бы с одной коллекцией.
    connected_cards = await conn.execute(
        select(CardCollectionTable.c.card_id).where(CardCollectionTable.c.card_id.in_(cards))
    )
    return set(connected_cards.scalars().all())


async def delete_collection(conn: AsyncConnection, collection_id: int) -> None:
    checking_cards: set[int] = set((await conn.execute(select(CardCollectionTable.c.card_id).where(
        CardCollectionTable.c.collection_id == collection_id
    ))).scalars().all())
    await conn.execute(delete(CollectionTable).where(CollectionTable.c.id == collection_id))
    await conn.commit()

    cards_with_collections: set[int] = await _filter_connected_cards(conn, checking_cards)
    need_delete_cards: list[int] = list(checking_cards.difference(cards_with_collections))
    if need_delete_cards:
        await delete_cards(conn, need_delete_cards)
