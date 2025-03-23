from fastapi import APIRouter, HTTPException, Response

from app import repositories
from app.schemas import Collection, CollectionCreate, CollectionShort

from app.api.dependencies import DBConnection, UserID


router = APIRouter(
    prefix="/collections",
    tags=["collection"]
)

#####
@router.get("/{collection_id}", response_model=Collection)
async def read_collection(conn: DBConnection, collection_id: int) -> Collection:
    collection: Collection | None = await repositories.get_collection(conn, collection_id)
    if collection is None:
        raise HTTPException(status_code=404, detail="Collection not found")
    return collection

#####
@router.get("/", response_model=list[CollectionShort], description="Returns collections' list without descriptions")
async def read_collections(conn: DBConnection, limit: int = 100, skip: int = 0) -> list[CollectionShort]:
    return await repositories.get_collections_short(conn, limit=limit, skip=skip)

#####
@router.post("/", response_model=Collection)
async def create_collection(conn: DBConnection, user_id: UserID, collection: CollectionCreate) -> Collection:
    try:
        await repositories.check_user_id(conn, user_id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    return await repositories.create_collection(conn, user_id, collection)

##
@router.delete("/{collection_id}", response_class=Response)
async def delete_collection(conn: DBConnection, user_id: UserID, collection_id: int):
    try:
        await repositories.check_user_id(conn, user_id)
        await repositories.check_user_collection_id(conn, user_id, collection_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    await repositories.delete_collection(conn, collection_id)
    return Response(status_code=200)

#####
@router.put("/{collection_id}", response_model=Collection)
async def update_collection(
        conn: DBConnection, user_id: UserID, collection_id: int, new_collection: CollectionCreate
) -> Collection:
    try:
        await repositories.check_user_id(conn, user_id)
        await repositories.check_user_collection_id(conn, user_id, collection_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    return await repositories.update_collection(conn, collection_id, new_collection)

#####
@router.get("/{collection_id}/cards", response_model=list[int])
async def read_collection_cards(conn: DBConnection, collection_id: int) -> list[int]:
    try:
        await repositories.check_collection_id(conn, collection_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    return await repositories.get_collection_cards(conn, collection_id)


@router.get("/{collection_id}/cards/train", response_model=list[int])
async def train_cards(
        conn: DBConnection, user_id: UserID, collection_id: int
) -> list[int]:
    try:
        await repositories.check_user_id(conn, user_id)
        await repositories.check_collection_id(conn, collection_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    return await repositories.get_training_cards(conn, user_id, collection_id)
