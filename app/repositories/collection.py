from sqlalchemy import and_
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

    async def update_collection_by_id(
            self, collection_id: int, update_values: dict, output_schema: Type[SchemaType]
    ) -> SchemaType:
        return await self.update_one(self._item_id_filter(collection_id), update_values, output_schema)

    async def exists_collection_with_owner(self, owner_id: int, collection_id: int) -> bool:
        return await self.exists(
            and_(self.table.c.owner_id == owner_id, self._item_id_filter(collection_id))
        )


"""

"""


async def check_collection_id(conn: AsyncConnection, collection_id: int) -> None:
    result = await conn.execute(select(exists().where(CollectionTable.c.id == collection_id)))
    if not result.scalar():
        raise ValueError("Collection not found")


async def get_user_collections_short(
        conn: AsyncConnection, user_id: int, limit: int | None, skip: int
) -> list[CollectionShort]:
    query = select(CollectionTable.c[*CollectionShort.model_fields]).where(
        CollectionTable.c.owner_id == user_id).offset(skip)
    if limit is not None:
        query = query.limit(limit)
    result = await conn.execute(query)
    return [CollectionShort(**collection) for collection in result.mappings().all()]


async def _filter_connected_cards(conn: AsyncConnection, cards: set[int]) -> set[int]:
    """
    Фильтрует исходное множество идентификаторов карт, оставляя только те,
    которые имеют связь хотя бы с одной коллекцией в таблице CardCollectionTable.

    :param conn: Асинхронное соединение с базой данных.
    :param cards: Исходное множество идентификаторов карт.
    :return: Множество идентификаторов карт, которые имеют связь хотя бы с одной коллекцией.
    """
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
