from fastapi import HTTPException

from app.db import UnitOfWork
from app.repositories import CardCollectionRepository, CollectionRepository, UserRepository
from app.schemas import Collection, CollectionCreate, CollectionShort


__all__ = ["CollectionService"]


class CollectionService:
    async def add_collection(
            self, uow: UnitOfWork, user_id: int, collection: CollectionCreate
    ) -> Collection:
        async with uow.begin():
            user_repo = uow.get_repository(UserRepository)
            if not await user_repo.exists_user_with_id(user_id):
                raise HTTPException(status_code=400)  ## ТУТ ДОЛЖНО БЫТЬ КАСТОМНОЕ ИСКЛЮЧЕНИЕ!
            collection_data = collection.model_dump()
            collection_data["owner_id"] = user_id
            collection_repo = uow.get_repository(CollectionRepository)
            return await collection_repo.create_one(collection_data, Collection)

    async def get_collection(self, uow: UnitOfWork, collection_id: int) -> Collection:
        async with uow.begin():
            collection_repo = uow.get_repository(CollectionRepository)
            collection = await collection_repo.get_collection_by_id(collection_id, Collection)
            if collection is None:
                raise HTTPException(status_code=400)  ## ТУТ ДОЛЖНО БЫТЬ КАСТОМНОЕ ИСКЛЮЧЕНИЕ!
            return collection

    async def get_collections(
            self, uow: UnitOfWork, limit: int, offset: int
    ) -> list[CollectionShort]:
        async with uow.begin():
            collection_repo = uow.get_repository(CollectionRepository)
            return await collection_repo.get_all(CollectionShort, limit, offset)

    async def get_collection_cards(self, uow: UnitOfWork, collection_id: int) -> list[int]:
        async with uow.begin():
            collection_repo = uow.get_repository(CollectionRepository)
            if not await collection_repo.exists_collection_with_id(collection_id):
                raise HTTPException(status_code=400)  ## ТУТ ДОЛЖНО БЫТЬ КАСТОМНОЕ ИСКЛЮЧЕНИЕ!
            return await uow.get_repository(CardCollectionRepository).get_collection_cards(collection_id)

    async def update_user_collection(
            self, uow: UnitOfWork, user_id: int, collection_id: int, new_collection: CollectionCreate
    ) -> Collection:
        async with uow.begin():
            if not await uow.get_repository(UserRepository).exists_user_with_id(user_id):
                raise HTTPException(status_code=400)  ## ТУТ ДОЛЖНО БЫТЬ КАСТОМНОЕ ИСКЛЮЧЕНИЕ!
            collection_repo = uow.get_repository(CollectionRepository)
            if not await collection_repo.exists_collection_with_owner(user_id, collection_id):
                raise HTTPException(status_code=400)  ## ТУТ ДОЛЖНО БЫТЬ КАСТОМНОЕ ИСКЛЮЧЕНИЕ!
            collection_data = new_collection.model_dump()
            return await collection_repo.update_collection_by_id(
                collection_id, collection_data, Collection
            )

    async def delete_collection(self, uow: UnitOfWork, user_id: int, collection_id: int) -> None:
        async with (uow.begin()):
            if not await uow.get_repository(UserRepository).exists_user_with_id(user_id):
                raise HTTPException(status_code=400)  ## ТУТ ДОЛЖНО БЫТЬ КАСТОМНОЕ ИСКЛЮЧЕНИЕ!
            collection_repo = uow.get_repository(CollectionRepository)
            if not await collection_repo.exists_collection_with_owner(user_id, collection_id):
                raise HTTPException(status_code=400)  ## ТУТ ДОЛЖНО БЫТЬ КАСТОМНОЕ ИСКЛЮЧЕНИЕ!
            card_collection_repo = uow.get_repository(CardCollectionRepository)
            collection_cards = set(await card_collection_repo.get_collection_cards(collection_id))
            await collection_repo.delete_collection(collection_id)
            cards_with_collections = await card_collection_repo.filter_cards_with_collection(collection_cards)
            if cards_without_collections := list(collection_cards.difference(cards_with_collections)):
                """await delete_cards(conn, need_delete_cards)"""

"""
async def delete_collection(conn: AsyncConnection, collection_id: int) -> None:
    checking_cards: set[int] = set((await conn.execute(select(CardCollectionTable.c.card_id).where(
        CardCollectionTable.c.collection_id == collection_id
    ))).scalars().all())
    await conn.execute(delete(CollectionTable).where(CollectionTable.c.id == collection_id))
    await conn.commit()

    cards_with_collections: set[int] = await filter_cards_with_collection(conn, checking_cards)
    need_delete_cards: list[int] = list(checking_cards.difference(cards_with_collections))
    if need_delete_cards:
        await delete_cards(conn, need_delete_cards)
"""
