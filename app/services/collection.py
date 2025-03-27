from fastapi import HTTPException

from app.schemas import Collection, CollectionCreate, CollectionShort
from app.repositories import (
    CardRepository, CardCollectionRepository, CollectionRepository,
    UserRepository, TrainRecordRepository
)

from .base import BaseService


__all__ = ["CollectionService"]


class CollectionService(BaseService):
    async def add_collection(self, user_id: int, collection: CollectionCreate) -> Collection:
        async with self.uow.begin():
            if not await self.uow.get_repository(UserRepository).exists_user_with_id(user_id):
                raise HTTPException(status_code=400)  ## ТУТ ДОЛЖНО БЫТЬ КАСТОМНОЕ ИСКЛЮЧЕНИЕ!
            collection_data = collection.model_dump()
            collection_data["owner_id"] = user_id
            collection_repo = self.uow.get_repository(CollectionRepository)
            return await collection_repo.create_one(collection_data, Collection)

    async def get_collection(self,collection_id: int) -> Collection:
        async with self.uow.begin():
            collection_repo = self.uow.get_repository(CollectionRepository)
            collection = await collection_repo.get_collection_by_id(collection_id, Collection)
            if collection is None:
                raise HTTPException(status_code=400)  ## ТУТ ДОЛЖНО БЫТЬ КАСТОМНОЕ ИСКЛЮЧЕНИЕ!
            return collection

    async def get_collections(self, limit: int, offset: int) -> list[CollectionShort]:
        async with self.uow.begin():
            collection_repo = self.uow.get_repository(CollectionRepository)
            return await collection_repo.get_all(CollectionShort, limit, offset)

    async def get_collection_cards(self, collection_id: int) -> list[int]:
        async with self.uow.begin():
            collection_repo = self.uow.get_repository(CollectionRepository)
            if not await collection_repo.exists_collection_with_id(collection_id):
                raise HTTPException(status_code=400)  ## ТУТ ДОЛЖНО БЫТЬ КАСТОМНОЕ ИСКЛЮЧЕНИЕ!
            return await self.uow.get_repository(CardCollectionRepository).get_collection_cards(collection_id)

    async def update_user_collection(
            self, user_id: int, collection_id: int, new_collection: CollectionCreate
    ) -> Collection:
        async with self.uow.begin():
            collection_repo = self.uow.get_repository(CollectionRepository)
            if not await collection_repo.exists_collection_with_owner(user_id, collection_id):
                raise HTTPException(status_code=400)  ## ТУТ ДОЛЖНО БЫТЬ КАСТОМНОЕ ИСКЛЮЧЕНИЕ!
            return await collection_repo.update_collection_by_id(
                collection_id, new_collection.model_dump(), Collection
            )

    async def delete_collection(self, user_id: int, collection_id: int) -> None:
        async with self.uow.begin():
            collection_repo = self.uow.get_repository(CollectionRepository)
            if not await collection_repo.exists_collection_with_owner(user_id, collection_id):
                raise HTTPException(status_code=400)  ## ТУТ ДОЛЖНО БЫТЬ КАСТОМНОЕ ИСКЛЮЧЕНИЕ!
            card_collection_repo = self.uow.get_repository(CardCollectionRepository)
            collection_cards = set(await card_collection_repo.get_collection_cards(collection_id))
            await collection_repo.delete_collection(collection_id)
            cards_with_collections = await (card_collection_repo
                                            .filter_cards_with_collection(collection_cards))
            if cards_without_collections := collection_cards.difference(cards_with_collections):
                await self.uow.get_repository(CardRepository).delete_cards(list(cards_without_collections))

    async def get_collection_training_cards(self, user_id: int, collection_id: int) -> list[int]:
        async with self.uow.begin():
            if not await self.uow.get_repository(UserRepository).exists_user_with_id(user_id):
                raise HTTPException(status_code=400)  ## ТУТ ДОЛЖНО БЫТЬ КАСТОМНОЕ ИСКЛЮЧЕНИЕ!
            collection_repo = self.uow.get_repository(CollectionRepository)
            if not await collection_repo.exists_collection_with_id(collection_id):
                raise HTTPException(status_code=400)  ## ТУТ ДОЛЖНО БЫТЬ КАСТОМНОЕ ИСКЛЮЧЕНИЕ!
            card_collection_repo = self.uow.get_repository(CardCollectionRepository)
            cards = await card_collection_repo.get_collection_cards(collection_id)
            train_record_repo = self.uow.get_repository(TrainRecordRepository)
            return await train_record_repo.get_collection_training_cards(user_id, cards)
