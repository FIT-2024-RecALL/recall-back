from fastapi import APIRouter, Response

from app.schemas import Collection, CollectionCreate, CollectionShort

from .dependencies import CollectionServiceDep, UserIdDep


router = APIRouter(
    prefix="/collections",
    tags=["collection"]
)


@router.get("/{collection_id}", response_model=Collection)
async def read_collection(
        collection_id: int, collection_service: CollectionServiceDep
) -> Collection:
    return await collection_service.get_collection(collection_id)


@router.get("/", response_model=list[CollectionShort], description="Returns collections' list without descriptions")
async def read_collections(
        collection_service: CollectionServiceDep, limit: int = 100, skip: int = 0
) -> list[CollectionShort]:
    return await collection_service.get_collections(limit, skip)


@router.get("/{collection_id}/cards", response_model=list[int])
async def read_collection_cards(
        collection_id: int, collection_service: CollectionServiceDep
) -> list[int]:
    return await collection_service.get_collection_cards(collection_id)


@router.get("/{collection_id}/cards/train", response_model=list[int])
async def train_cards(
        user_id: UserIdDep, collection_id: int, collection_service: CollectionServiceDep
) -> list[int]:
    return await collection_service.get_collection_training_cards(user_id, collection_id)


@router.post("/", response_model=Collection)
async def create_collection(
        user_id: UserIdDep, collection: CollectionCreate, collection_service: CollectionServiceDep
) -> Collection:
    return await collection_service.add_collection(user_id, collection)


@router.put("/{collection_id}", response_model=Collection)
async def update_collection(
        user_id: UserIdDep, collection_id: int, new_collection: CollectionCreate,
        collection_service: CollectionServiceDep
) -> Collection:
    return await collection_service.update_user_collection(user_id, collection_id, new_collection)


@router.delete("/{collection_id}", response_class=Response)
async def delete_collection(
        user_id: UserIdDep, collection_id: int, collection_service: CollectionServiceDep
):
    return await collection_service.delete_collection(user_id, collection_id)
