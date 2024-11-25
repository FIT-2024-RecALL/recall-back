from fastapi import APIRouter, HTTPException, Response

from app import crud, DBConnection, UserID
from app.schemas import Card, CardCreate


router = APIRouter(
    prefix="/cards",
    tags=["card"]
)


@router.get("/{card_id}", response_model=Card)
async def read_card(conn: DBConnection, card_id: int):
    card = await crud.get_card(conn, card_id)
    if card is None:
        raise HTTPException(status_code=404, detail="Card not found")
    return card


@router.get("/", response_model=list[Card])
async def read_cards(conn: DBConnection, skip: int = 0, limit: int | None = None):
    return await crud.get_cards(conn, limit=limit, skip=skip)


@router.post("/", response_model=Card)
async def create_card(conn: DBConnection, user_id: UserID, card: CardCreate):
    try:
        await crud.check_user_id(conn, user_id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    return await crud.create_card(conn, user_id, card)


@router.delete("/{card_id}", response_class=Response)
async def delete_card(conn: DBConnection, card_id: int):
    try:
        await crud.check_card_id(conn, card_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    await crud.delete_card(conn, card_id)
    await crud.delete_card_collection_by_card(conn, card_id)
    await crud.delete_train_record_by_card(conn, card_id)
    return Response(status_code=200)
