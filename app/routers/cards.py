from fastapi import APIRouter, HTTPException, Response

from app import crud
from app.helpers import DBConnection, IntList, UserID
from app.schemas import Card, CardCreate, CollectionShort


router = APIRouter(
    prefix="/cards",
    tags=["card"]
)


@router.get("/{card_id}", response_model=Card)
async def read_card(conn: DBConnection, card_id: int):
    card: Card | None = await crud.get_card(conn, card_id)
    if card is None:
        raise HTTPException(status_code=404, detail="Card not found")
    return card


@router.post("/", response_model=Card)
async def create_card(
        conn: DBConnection, user_id: UserID, card: CardCreate, collections: IntList
) -> Card:
    result_card: Card = await crud.create_card(conn, user_id, card)
    try:
        await crud.check_user_id(conn, user_id)
        await crud.create_card_collection_connections(conn, user_id, result_card.id, collections)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    return result_card


@router.delete("/{card_id}", response_class=Response)
async def delete_card(conn: DBConnection, user_id: UserID, card_id: int):
    try:
        await crud.check_user_id(conn, user_id)
        await crud.check_user_card_id(conn, user_id, card_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    await crud.delete_card(conn, card_id)
    return Response(status_code=200)


@router.put("/{card_id}", response_model=Card)
async def update_card(
        conn: DBConnection, user_id: UserID, card_id: int,
        new_card: CardCreate, collections: IntList
) -> Card:
    try:
        await crud.check_user_id(conn, user_id)
        await crud.check_user_card_id(conn, user_id, card_id)
        await crud.update_card_collection_connections(conn, user_id, card_id, collections)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    return await crud.update_card(conn, card_id, new_card)


@router.get("/{card_id}/collections", response_model=list[CollectionShort])
async def read_card_collections(
        conn: DBConnection, user_id: UserID, card_id: int
) -> list[CollectionShort]:
    try:
        await crud.check_user_id(conn, user_id)
        await crud.check_user_card_id(conn, user_id, card_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    return await crud.get_user_card_collections(conn, user_id, card_id)
