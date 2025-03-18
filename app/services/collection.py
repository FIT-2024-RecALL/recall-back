from fastapi import HTTPException

from app.db import UnitOfWork
from app.repositories import CollectionRepository, UserRepository
from app.schemas import Collection, CollectionCreate, CollectionShort

__all__ = ["CollectionService"]


"""
@router.get("/collections", response_model=list[CollectionShort])
async def read_collections(
        conn: DBConnection, user_id: UserID, skip: int = 0, limit: int | None = None
) -> list[CollectionShort]:
    try:
        await repositories.check_user_id(conn, user_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    return await repositories.get_user_collections_short(conn, user_id, limit=limit, skip=skip)
"""

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

    async def get_collection(self, uow: UnitOfWork, collection_id: int) -> Collection:
        async with uow.begin():
            collection_repo = uow.get_repository(CollectionRepository)
            collection = await collection_repo.get_collection_by_id(collection_id, Collection)
            if collection is None:
                raise HTTPException(status_code=400)  ## ТУТ ДОЛЖНО БЫТЬ КАСТОМНОЕ ИСКЛЮЧЕНИЕ!
            return collection

    async def get_collections(self, uow: UnitOfWork, limit: int, offset: int) -> list[CollectionShort]:
        async with uow.begin():
            return await uow.get_repository(CollectionRepository).get_all(CollectionShort, limit, offset)

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


"""

"""
