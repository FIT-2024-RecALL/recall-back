from sqlalchemy import select, desc, text, func
from typing import Type

from app.db import TrainRecordTable

from .base import BaseSQLAlchemyRepository, SchemaType


__all__ = ["TrainRecordRepository"]


class TrainRecordRepository(BaseSQLAlchemyRepository):
    table = TrainRecordTable

    async def create_train_record(
            self, train_data: dict, interval_duration: int, output_schema: Type[SchemaType]
    ) -> SchemaType:
        repeat_date = func.now()
        repeat_interval = text(f"INTERVAL '{interval_duration} minutes'")
        train_data.update(repeat_date=repeat_date, next_repeat_date=repeat_date+repeat_interval)
        return await self.create_one(train_data, output_schema)

    async def get_user_card_last_train_record(
            self, user_id: int, card_id: int, output_schema: Type[SchemaType]
    ) -> SchemaType | None:
        result = (await self.connection.execute(
            select(self.table.c[*output_schema.fields()])
            .where(self.table.c.user_id == user_id, self.table.c.card_id == card_id)
            .order_by(desc(self.table.c.id)).limit(1)
        )).mappings().first()
        return result and output_schema(**result)

    async def get_collection_training_cards(
            self, user_id: int, collection_cards: list[int]
    ) -> list[int]:
        subquery = (
            select(self.table.c.card_id, func.max(self.table.c.id).label("last_id"))
            .where(self.table.c.card_id.in_(collection_cards), self.table.c.user_id == user_id)
            .group_by(self.table.c.card_id).subquery()
        )
        training_cards = await self.connection.execute(
            select(self.table.c.card_id).join(subquery, self.table.c.id == subquery.c.last_id)
            .where(self.table.c.next_repeat_date <= func.now())
        )
        return list(training_cards.scalars().all())
