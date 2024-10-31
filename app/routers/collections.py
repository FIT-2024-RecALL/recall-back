from fastapi import APIRouter, HTTPException

from app import crud, schemas
from app.dependencies import DBConnection, IntList


router = APIRouter(
    prefix="/collections",
    tags=["collection"]
)


@router.get("/{collection_id}", response_model=schemas.collection.Collection)
def read_collection(conn: DBConnection, collection_id: int):
    collection = crud.collection.get_collection(conn, collection_id)
    if collection is None:
        raise HTTPException(status_code=404, detail="Collection not found")
    return collection


@router.get("/", response_model=list[schemas.collection.Collection])
def read_collections(conn: DBConnection, limit: int = 100, skip: int = 0):
    return crud.collection.get_collections(conn, limit=limit, skip=skip)


@router.post("/{user_id}", response_model=schemas.collection.Collection)
def create_collection(
        conn: DBConnection, user_id: int, collection: schemas.collection.CollectionCreate
):
    try:
        created_collection = crud.collection.create_collection(conn, user_id, collection)
        return created_collection
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


##################### Нужно тестировать ########################

@router.get("/{collection_id}/cards", response_model=list[schemas.card.Card])
def read_collection_cards(conn: DBConnection, collection_id: int):
    return crud.card_collection.get_collection_cards(conn, collection_id)


@router.post("/{collection_id}/pair")
def set_card_collection_connection(conn: DBConnection, collection_id: int, cards: IntList):
    crud.card_collection.create_card_collection(conn, collection_id, cards)
    return "Done"


@router.delete("/{collection_id}/unpair")
def delete_card_collection_connection(
        conn: DBConnection, collection_id: int, cards: IntList
):
    crud.card_collection.delete_card_collection(conn, collection_id, cards)
    return "Done"
