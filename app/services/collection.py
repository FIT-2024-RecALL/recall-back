from fastapi import HTTPException

from app.db import UnitOfWork
from app.repositories import CollectionRepository, UserRepository
from app.schemas import Collection, CollectionCreate

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
            return await uow.get_repository(CollectionRepository).create_one(collection_data, Collection)

    async def get_collections(self, uow: UnitOfWork, collection_id: int) -> Collection:
        async with uow.begin():
            collection_repo = uow.get_repository(CollectionRepository)
            collection = await collection_repo.get_collection_by_id(collection_id, Collection)
            if collection is None:
                raise HTTPException(status_code=400)  ## ТУТ ДОЛЖНО БЫТЬ КАСТОМНОЕ ИСКЛЮЧЕНИЕ!
            return collection





"""



"""
