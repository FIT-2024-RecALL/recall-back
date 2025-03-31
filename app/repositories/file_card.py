from sqlalchemy import and_, select, insert, update
from typing import Type

from app.db.models import FileCardTable, FileTable, CardTable
from app.schemas import Card, FileScheme

from .base import BaseSQLAlchemyRepository, SchemaType


__all__ = ["FileCardRepository"]


class FileCardRepository(BaseSQLAlchemyRepository):
    file_table = FileTable
    card_table = CardTable
    table = FileCardTable

    async def __set_card_files_connections(
            self, card_id: int, file_ids: list[int]
    ) -> None:
        await self.connection.execute(
            insert(self.table),
            [{"card_id": card_id, "file_id": file_id} for file_id in file_ids],
        )

    async def __unset_card_files_connections(
            self, card_id: int, file_ids: list[int]
    ) -> None:
       await self.delete(
           and_(self.table.c.card_id == card_id, self.table.c.file_id.in_(file_ids))
       )

    async def __filter_owned_files(
            self, owner_id: int, file_ids: list[int]
    ) -> list[int]:
        result = await self.connection.execute(
            select(self.file_table.c.id).where(and_(
                self.file_table.c.id.in_(set(file_ids)),
                self.file_table.c.owner_id == owner_id
            ))
        )
        return list(result.scalars().all())

    async def update_card_files_connections(
            self, user_id: int, card_id: int, file_ids: list[int]
    ) -> bool:
        new_file_ids = set(await self.__filter_owned_files(user_id, file_ids))
        current_file_ids = set(await self.get_card_files_ids(card_id))
        files_connections_changed = False
        if deleted_file_ids := list(current_file_ids.difference(new_file_ids)):
            await self.__unset_card_files_connections(card_id, deleted_file_ids)
            files_connections_changed = True
        if not_inserted_file_ids := list(new_file_ids.difference(current_file_ids)):
            await self.__set_card_files_connections(card_id, not_inserted_file_ids)
            files_connections_changed = True
        return files_connections_changed

    async def get_card_files_ids(self, card_id: int) -> list[int]:
        result = await self.connection.execute(
            select(self.table.c.file_id).where(self.table.c.card_id == card_id)
        )
        return list(result.scalars().all())

    async def get_card_files(
            self, card_id: int, output_schema: Type[SchemaType]
    ) -> list[SchemaType]:
        result = await self.connection.execute(
            select(self.file_table.c[*output_schema.fields()])
                .join(self.table, self.file_table.c.id == self.table.c.file_id)
                .where(self.table.c.card_id == card_id)
        )
        return [output_schema(**elem) for elem in result.mappings().all()]

    async def get_file_cards_ids(self, file_id: int) -> list[int]:
        result = await self.connection.execute(
            select(self.table.c.card_id).where(self.table.c.file_id == file_id)
        )
        return list(result.scalars().all())

    async def get_file_cards(
            self, file_id: int, output_schema: Type[SchemaType]
    ) -> list[SchemaType]:
        result = await self.connection.execute(
            select(self.card_table.c[*output_schema.fields()])
                .join(self.table, self.card_table.c.id == self.table.c.card_id)
                .where(self.table.c.file_id == file_id)
        )
        return [output_schema(**elem) for elem in result.mappings().all()]
    
    async def __is_file_public_by_cards(self, file_id: int) -> bool:
        for card in await self.get_file_cards(file_id, Card):
            if card.is_public:
                return True
        return False

    async def refresh_file_publicity(self, file_id: int) -> FileScheme:
        is_public_new = await self.__is_file_public_by_cards(file_id)
        result = await self.connection.execute(
            update(self.file_table)
                .where(self.file_table.c.id == file_id)
                .values(is_public=is_public_new)
                .returning(self.file_table.c[*FileScheme.fields()])
        )
        return FileScheme(**result.mappings().first())
    
    async def update_files_publicity(
            self, card_id: int, is_public: bool
    ) -> list[FileScheme]:
        if is_public:
            result = await self.connection.execute(
                update(self.file_table)
                    .where(self.file_table.c.id == self.table.c.file_id)
                    .where(self.table.c.card_id == card_id)
                    .values(is_public=True)
                .returning(self.file_table.c[*FileScheme.fields()])
            )
            return [FileScheme(**elem) for elem in result.mappings().all()]
        else:
            return [
                await self.refresh_file_publicity(file_id)
                for file_id in await self.get_card_files_ids(card_id)
            ]
