from fastapi import APIRouter, Response

from app.schemas import Card, CardCreate, CollectionShort, FileMeta

from .dependencies import CardServiceDep, IntListBody, UserIdDep, UserIdSoftDep


router = APIRouter(
    prefix="/cards",
    tags=["card"]
)


@router.get("/{card_id}", response_model=Card)
async def read_card(card_id: int, user_id: UserIdSoftDep, card_service: CardServiceDep):
    return await card_service.get_card(card_id, user_id)


@router.get("/{card_id}/collections", response_model=list[CollectionShort])
async def read_card_collections(
        user_id: UserIdDep, card_id: int, card_service: CardServiceDep
):
    return await card_service.get_card_collections(user_id, card_id)

@router.get("/{card_id}/files", response_model=list[FileMeta])
async def read_card_files(
        user_id: UserIdDep, card_id: int, card_service: CardServiceDep
):
    return await card_service.get_card_files(card_id, user_id)

@router.post("/", response_model=Card)
async def create_card(
        user_id: UserIdDep, card: CardCreate, collections: IntListBody, card_service: CardServiceDep
):
    return await card_service.add_card(user_id, collections, card)


@router.put("/{card_id}", response_model=Card)
async def update_card(
        user_id: UserIdDep, card_id: int, new_card: CardCreate, collections: IntListBody,
        card_service: CardServiceDep
):
    return await card_service.update_user_card(user_id, card_id, new_card, collections)


@router.delete("/{card_id}", response_class=Response)
async def delete_card(
        user_id: UserIdDep, card_id: int, card_service: CardServiceDep
):
    await card_service.delete_card(user_id, card_id)
