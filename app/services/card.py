from fastapi import HTTPException

from app.db import UnitOfWork
from app.repositories import CardCollectionRepository, UserRepository, CardRepository
from app.schemas import Card, CardCreate


"""
## CARD SERVICE
async def update_card_collection_connections(
        conn: AsyncConnection, user_id: int, card_id: int, collections: list[int]
) -> None:
    request_collections: set[int] = set(await filter_exist_owner_collections(conn, user_id, collections))
    if not request_collections:
        raise ValueError("Collections not found")
    old_collections: set[int] = set(await fetch_card_collections(conn, card_id))
    delete_collections: list[int] = list(old_collections.difference(request_collections))
    new_collections: list[int] = list(request_collections.difference(old_collections))
    if delete_collections:
        await unset_card_collection_connections(conn, card_id, delete_collections)
    if new_collections:
        await set_card_collection_connections(conn, card_id, new_collections)
"""


class CardService:
    @staticmethod
    async def __create_connections(
            card_collection_repo: CardCollectionRepository,
            owner_id: int, card_id: int, collections: list[int]
    ) -> None:
        new_collections = await (card_collection_repo
                                 .filter_owner_exist_collections(owner_id, collections))
        if not new_collections:
            raise HTTPException(status_code=400)  ## ТУТ ДОЛЖНО БЫТЬ КАСТОМНОЕ ИСКЛЮЧЕНИЕ!
        await card_collection_repo.set_card_collection_connections(card_id, collections)

    async def add_card(
            self, uow: UnitOfWork, user_id: int, collections: list[int], card: CardCreate
    ) -> Card:
        async with uow.begin():
            if not await uow.get_repository(UserRepository).exists_user_with_id(user_id):
                raise HTTPException(status_code=400)  ## ТУТ ДОЛЖНО БЫТЬ КАСТОМНОЕ ИСКЛЮЧЕНИЕ!
            card_data = card.model_dump()
            card_data["owner_id"] = user_id
            new_card = await uow.get_repository(CardRepository).create_one(card_data, Card)
            await self.__create_connections(
                uow.get_repository(CardCollectionRepository), user_id, new_card.id, collections)
            return new_card

""" 
async def get_card(conn: AsyncConnection, card_id: int) -> Card | None:
    result = (await conn.execute(
        select(CardTable.c[*Card.model_fields]).where(CardTable.c.id == card_id)
    )).mappings().first()
    return result if result is None else Card(**result)

@router.get("/{card_id}", response_model=Card)
async def read_card(conn: DBConnection, card_id: int):
    card: Card | None = await repositories.get_card(conn, card_id)
    if card is None:
        raise HTTPException(status_code=404, detail="Card not found")
    return card
"""
