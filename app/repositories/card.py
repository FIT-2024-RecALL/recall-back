from sqlalchemy import and_, select, delete, update, exists
from typing import Type

from app.db import CardTable

from .base import BaseSQLAlchemyRepository, SchemaType


__all__ = ["CardRepository"]


class CardRepository(BaseSQLAlchemyRepository):
    table = CardTable

    async def get_card_by_id(
            self, card_id: int, output_schema: Type[SchemaType]
    ) -> SchemaType | None:
        return await self.get_one_or_none(self._item_id_filter(card_id), output_schema)

    async def get_owner_cards(self, owner_id: int, limit: int | None, offset: int) -> list[int]:
        query = select(self.table.c.id).where(self.table.c.owner_id == owner_id).offset(offset)
        if limit is not None:
            query = query.limit(limit)
        result = await self.connection.execute(query)
        return list(result.scalars().all())

    async def update_card_by_id(
            self, card_id: int, update_values: dict, output_schema: Type[SchemaType]
    ) -> SchemaType:
        return await self.update_one(self._item_id_filter(card_id), update_values, output_schema)

    async def delete_card(self, card_id: int) -> None:
        await self.delete(self._item_id_filter(card_id))

    async def delete_cards(self, cards: list[int]) -> None:
        await self.delete(self.table.c.id.in_(cards))

    async def exists_card_with_id(self, card_id: int) -> bool:
        return await self.exists(self._item_id_filter(card_id))

    async def exists_card_with_owner(self, owner_id: int, card_id: int) -> bool:
        return await self.exists(
            and_(self.table.c.owner_id == owner_id, self._item_id_filter(card_id))
        )
