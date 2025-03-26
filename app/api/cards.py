from fastapi import APIRouter, Response

from app.schemas import Card, CardCreate, CollectionShort

from .dependencies import CardServiceDep, IntListBody, UserIdDep, UnitOfWorkDep

router = APIRouter(
    prefix="/cards",
    tags=["card"]
)


@router.get("/{card_id}", response_model=Card)
async def read_card(card_id: int, card_service: CardServiceDep, uow: UnitOfWorkDep):
    return await card_service.get_card(uow, card_id)


@router.get("/{card_id}/collections", response_model=list[CollectionShort])
async def read_card_collections(
        user_id: UserIdDep, card_id: int, card_service: CardServiceDep, uow: UnitOfWorkDep
):
    return card_service.get_card_collections(uow, user_id, card_id)


@router.post("/", response_model=Card)
async def create_card(
        user_id: UserIdDep, card: CardCreate, collections: IntListBody,
        card_service: CardServiceDep, uow: UnitOfWorkDep
):
    return card_service.add_card(uow, user_id, collections, card)


@router.put("/{card_id}", response_model=Card)
async def update_card(
        user_id: UserIdDep, card_id: int, new_card: CardCreate, collections: IntListBody,
        card_service: CardServiceDep, uow: UnitOfWorkDep
):
    return card_service.update_user_card(uow, user_id, card_id, new_card, collections)


@router.delete("/{card_id}", response_class=Response)
async def delete_card(
        user_id: UserIdDep, card_id: int, card_service: CardServiceDep, uow: UnitOfWorkDep
):
    await card_service.delete_card(uow, user_id, card_id)
