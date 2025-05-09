from typing import Optional
from fastapi import HTTPException

from app.schemas import Collection, CollectionCreate, CollectionShort, PublicStatusMixin
from app.repositories import (
    CardRepository, CardCollectionRepository, CollectionRepository,
    UserRepository, TrainRecordRepository, FileCardRepository
)

from .base import BaseService, with_unit_of_work


__all__ = ["CollectionService"]


class CollectionService(BaseService):
    @with_unit_of_work
    async def add_collection(self, user_id: int, collection: CollectionCreate) -> Collection:
        if not await self.uow.get_repository(UserRepository).exists_user_with_id(user_id):
            raise HTTPException(status_code=401, detail="Authorized user doesn't exist")
        collection_data = collection.model_dump()
        collection_data["owner_id"] = user_id
        collection_repo = self.uow.get_repository(CollectionRepository)
        return await collection_repo.create_one(collection_data, Collection)

    @with_unit_of_work
    async def get_collection(self, collection_id: int, user_id: int | None) -> Collection:
        collection_repo = self.uow.get_repository(CollectionRepository)
        collection = await collection_repo.get_collection_by_id(collection_id, Collection)
        if collection is None:
            raise HTTPException(status_code=404, detail="Collection not found")
        if not collection.is_public and collection.owner_id != user_id:
            raise HTTPException(status_code=403, detail="This collection is private")
        return collection

    @with_unit_of_work
    async def get_collections(self, user_id: int | None, limit: int, offset: int) -> list[CollectionShort]:
        collection_repo = self.uow.get_repository(CollectionRepository)
        return await collection_repo.get_all_visible_collections(
            user_id, CollectionShort, limit, offset
        )

    @with_unit_of_work
    async def get_collection_cards(self, collection_id: int, user_id: int | None) -> list[int]:
        await self.get_collection(collection_id, user_id) # Проверка существования коллекции и правтности
        return await self.uow.get_repository(CardCollectionRepository).get_collection_cards(collection_id)

    @with_unit_of_work
    async def update_user_collection(
            self, user_id: int, collection_id: int, new_collection: CollectionCreate
    ) -> Collection:
        collection_repo = self.uow.get_repository(CollectionRepository)
        if not await collection_repo.exists_collection_with_owner(user_id, collection_id):
            raise HTTPException(status_code=401, detail="Only authorized owners can edit collections")
        return await collection_repo.update_collection_by_id(
            collection_id, new_collection.model_dump(), Collection
        )
    
    @with_unit_of_work
    async def update_publicity(
            self, user_id: int, collection_id: int, is_public: bool
    ) -> Collection:
        collection_repo = self.uow.get_repository(CollectionRepository)
        if not await collection_repo.exists_collection_with_owner(user_id, collection_id):
            raise HTTPException(status_code=401, detail="Only authorized owners can change their collections' publicity")
        collection = await collection_repo.update_collection_by_id(
            collection_id, {'is_public': is_public}, Collection
        )
        card_collection_repo = self.uow.get_repository(CardCollectionRepository)
        for updated_card in await card_collection_repo.update_cards_publicity(
            collection_id, is_public, PublicStatusMixin
        ):
            await self.uow.get_repository(FileCardRepository).update_files_publicity(
                updated_card.id, updated_card.is_public, PublicStatusMixin
            )
        return collection

    @with_unit_of_work
    async def delete_collection(self, user_id: int, collection_id: int) -> None:
        collection_repo = self.uow.get_repository(CollectionRepository)
        if not await collection_repo.exists_collection_with_owner(user_id, collection_id):
            raise HTTPException(status_code=401, detail="Only authorized owners can delete collections")
        card_collection_repo = self.uow.get_repository(CardCollectionRepository)
        collection_cards = set(await card_collection_repo.get_collection_cards(collection_id))
        await collection_repo.delete_collection(collection_id)
        cards_with_collections = await (card_collection_repo
                                        .filter_cards_with_collection(collection_cards))
        if cards_without_collections := collection_cards.difference(cards_with_collections):
            await self.uow.get_repository(CardRepository).delete_cards(list(cards_without_collections))
        for card_id in cards_with_collections:
            updated_card = await card_collection_repo.refresh_card_publicity(card_id, PublicStatusMixin)
            await self.uow.get_repository(FileCardRepository).update_files_publicity(
                updated_card.id, updated_card.is_public, PublicStatusMixin
            )

    @with_unit_of_work
    async def get_collection_training_cards(self, user_id: int, collection_id: int) -> list[int]:
        if not await self.uow.get_repository(UserRepository).exists_user_with_id(user_id):
            raise HTTPException(status_code=401, detail="Only authorized users can train collections")
        await self.get_collection(collection_id, user_id) # Проверка существования коллекции и правтности
        card_collection_repo = self.uow.get_repository(CardCollectionRepository)
        cards = await card_collection_repo.get_collection_cards(collection_id)
        train_record_repo = self.uow.get_repository(TrainRecordRepository)
        return await train_record_repo.get_collection_training_cards(user_id, cards)
