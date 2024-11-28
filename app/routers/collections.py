from fastapi import APIRouter, HTTPException, Response

from app import crud, DBConnection, IntList, UserID
from app.schemas import Card, Collection, CollectionCreate


router = APIRouter(
    prefix="/collections",
    tags=["collection"]
)


### ПЕРЕПИСАТЬ ДЛЯ ПОЛЬЗОВАТЕЛЯ
@router.get("/{collection_id}", response_model=Collection)
async def read_collection(conn: DBConnection, collection_id: int):
    collection = await crud.get_collection(conn, collection_id)
    if collection is None:
        raise HTTPException(status_code=404, detail="Collection not found")
    return collection


### ПЕРЕПИСАТЬ ДЛЯ ПОЛЬЗОВАТЕЛЯ
@router.get("/", response_model=list[Collection])
async def read_collections(conn: DBConnection, skip: int = 0, limit: int | None = None):
    return await crud.get_collections(conn, limit=limit, skip=skip)


@router.post("/", response_model=Collection)
async def create_collection(conn: DBConnection, user_id: UserID, collection: CollectionCreate):
    try:
        await crud.check_user_id(conn, user_id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    return await crud.create_collection(conn, user_id, collection)


### UPDATE AND DELETE


@router.get("/{collection_id}/cards", response_model=list[Card])
async def read_collection_cards(
        conn: DBConnection, user_id: UserID, collection_id: int
) -> list[Card]:
    try:
        await crud.check_user_id(conn, user_id)
        await crud.check_collection_id(conn, collection_id) ################
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    return await crud.get_user_collection_cards(conn, user_id, collection_id)


@router.get("/{card_id}/collections")
async def read_card_collections(
        conn: DBConnection, user_id: UserID, card_id: int
) -> list[Collection]:
    try:
        await crud.check_user_id(conn, user_id)
        await crud.check_card_id(conn, user_id, card_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    return await crud.get_user_card_collections(conn, user_id, card_id)
