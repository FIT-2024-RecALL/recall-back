from typing import Optional

from fastapi import HTTPException

from app.repositories import CardCollectionRepository, UserRepository, CardRepository
from app.schemas import Card, CardCreate, CollectionShort

from .base import BaseService, with_unit_of_work


__all__ = ["CardService"]


class CardService(BaseService):
    @staticmethod
    async def __create_connections(
            card_collection_repo: CardCollectionRepository,
            owner_id: int, card_id: int, collections: list[int]
    ) -> None:
        new_collections = await (card_collection_repo
                                 .filter_owner_exist_collections(owner_id, collections))
        if not new_collections:
            raise HTTPException(status_code=409, detail="Invalid collections")
        await card_collection_repo.set_card_collection_connections(card_id, new_collections)

    @staticmethod
    async def __update_connections(
            card_collection_repo: CardCollectionRepository,
            owner_id: int, card_id: int, collections: list[int]
    ) -> None:
        request_collections = set(await card_collection_repo
                                  .filter_owner_exist_collections(owner_id, collections))
        if not request_collections:
            raise HTTPException(status_code=409, detail="Invalid collections")
        old_collections = set(await card_collection_repo.fetch_card_collections(card_id))
        if delete_collections := list(old_collections.difference(request_collections)):
            await (card_collection_repo
                   .unset_card_collection_connections(card_id, delete_collections))
        if new_collections := list(request_collections.difference(old_collections)):
            await card_collection_repo.set_card_collection_connections(card_id, new_collections)

    @with_unit_of_work
    async def add_card(self, user_id: int, collections: list[int], card: CardCreate) -> Card:
        if not await self.uow.get_repository(UserRepository).exists_user_with_id(user_id):
            raise HTTPException(status_code=401, detail="Authorized user doesn't exist")
        card_data = card.model_dump()
        card_data["owner_id"] = user_id
        new_card = await self.uow.get_repository(CardRepository).create_one(card_data, Card)
        await self.__create_connections(
            self.uow.get_repository(CardCollectionRepository), user_id, new_card.id, collections)
        return new_card

    @with_unit_of_work
    async def get_card(self, card_id: int, user_id: Optional[int]) -> Card:
        card = await self.uow.get_repository(CardRepository).get_card_by_id(card_id, Card)
        if card is None:
            raise HTTPException(status_code=404, detail="Card not found")
        if not card.is_public and card.owner_id is not user_id:
            raise HTTPException(status_code=403, detail="This card is private")
        return card

    @with_unit_of_work
    async def get_card_collections(self, user_id: int, card_id: int) -> list[CollectionShort]:
        card_repo = self.uow.get_repository(CardRepository)
        if not await card_repo.exists_card_with_owner(user_id, card_id):
            raise HTTPException(status_code=401, detail="Only authorized owners can get cards' collections")
        card_collection_repo = self.uow.get_repository(CardCollectionRepository)
        return await card_collection_repo.get_card_collections(card_id, CollectionShort)

    @with_unit_of_work
    async def update_user_card(
            self, user_id: int, card_id: int, new_card: CardCreate, collections: list[int]
    ) -> Card:
        card_repo = self.uow.get_repository(CardRepository)
        if not await card_repo.exists_card_with_owner(user_id, card_id):
            raise HTTPException(status_code=401, detail="Only authorized owners can edit cards")
        await self.__update_connections(
            self.uow.get_repository(CardCollectionRepository), user_id, card_id, collections)
        return await card_repo.update_card_by_id(card_id, new_card.model_dump(), Card)

    @with_unit_of_work
    async def delete_card(self, user_id: int, card_id: int) -> None:
        card_repo = self.uow.get_repository(CardRepository)
        if not await card_repo.exists_card_with_owner(user_id, card_id):
            raise HTTPException(status_code=401, detail="Only authorized owners can delete cards")
        await card_repo.delete_card(card_id)
