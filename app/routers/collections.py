from fastapi import APIRouter, HTTPException, Response

from app import crud, DBConnection, IntList, UserID
from app.schemas import Card, Collection, CollectionCreate


router = APIRouter(
    prefix="/collections",
    tags=["collection"]
)


@router.get("/{collection_id}", response_model=Collection)
async def read_collection(conn: DBConnection, collection_id: int):
    collection = await crud.get_collection(conn, collection_id)
    if collection is None:
        raise HTTPException(status_code=404, detail="Collection not found")
    return collection


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


@router.get("/{collection_id}/cards", response_model=list[Card])
async def read_collection_cards(conn: DBConnection, collection_id: int):
    try:
        await crud.check_collection_id(conn, collection_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    return await crud.get_collection_cards(conn, collection_id)


@router.post("/{collection_id}/pair", response_class=Response)
async def set_card_collection_connection(conn: DBConnection, collection_id: int, cards: IntList):
    try:
        await crud.check_collection_id(conn, collection_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    await crud.create_card_collection(conn, collection_id, cards)
    return Response(status_code=200)


@router.delete("/{collection_id}/unpair", response_class=Response)
async def delete_card_collection_connection(conn: DBConnection, collection_id: int, cards: IntList):
    await crud.delete_card_collection(conn, collection_id, cards)
    return Response(status_code=200)
