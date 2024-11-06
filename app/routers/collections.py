from fastapi import APIRouter, HTTPException

from app import crud
from app.dependencies import DBConnection, IntList
from app.schemas.card import Card
from app.schemas.collection import Collection, CollectionCreate


router = APIRouter(
    prefix="/collections",
    tags=["collection"]
)


@router.get("/{collection_id}", response_model=Collection)
async def read_collection(conn: DBConnection, collection_id: int):
    collection = await crud.collection.get_collection(conn, collection_id)
    if collection is None:
        raise HTTPException(status_code=404, detail="Collection not found")
    return collection


@router.get("/", response_model=list[Collection])
async def read_collections(conn: DBConnection, limit: int = 100, skip: int = 0):
    return await crud.collection.get_collections(conn, limit=limit, skip=skip)


@router.post("/{user_id}", response_model=Collection)
async def create_collection(conn: DBConnection, user_id: int, collection: CollectionCreate):
    try:
        created_collection = await crud.collection.create_collection(conn, user_id, collection)
        return created_collection
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/{collection_id}/cards", response_model=list[Card])
async def read_collection_cards(conn: DBConnection, collection_id: int):
    return await crud.card_collection.get_collection_cards(conn, collection_id)


@router.post("/{collection_id}/pair")
async def set_card_collection_connection(conn: DBConnection, collection_id: int, cards: IntList):
    await crud.card_collection.create_card_collection(conn, collection_id, cards)
    return "Done"


@router.delete("/{collection_id}/unpair")
async def delete_card_collection_connection(conn: DBConnection, collection_id: int, cards: IntList):
    await crud.card_collection.delete_card_collection(conn, collection_id, cards)
    return "Done"
