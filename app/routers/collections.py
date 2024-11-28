from fastapi import APIRouter, HTTPException, Response

from app import crud, DBConnection, IntList, UserID
from app.schemas import Card, Collection, CollectionCreate


router = APIRouter(
    prefix="/collections",
    tags=["collection"]
)


@router.get("/{collection_id}", response_model=Collection)
async def read_collection(conn: DBConnection, user_id: UserID, collection_id: int):
    try:
        await crud.check_user_id(conn, user_id)
        await crud.check_collection_id(conn, user_id, collection_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    return await crud.get_collection(conn, collection_id)


@router.get("/", response_model=list[Collection])
async def read_collections(
        conn: DBConnection, user_id: UserID, skip: int = 0, limit: int | None = None
) -> list[Collection]:
    try:
        await crud.check_user_id(conn, user_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    return await crud.get_user_collections(conn, user_id, limit=limit, skip=skip)


@router.post("/", response_model=Collection)
async def create_collection(conn: DBConnection, user_id: UserID, collection: CollectionCreate):
    try:
        await crud.check_user_id(conn, user_id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    return await crud.create_collection(conn, user_id, collection)


@router.delete("/{collection_id}", response_class=Response)
async def delete_collection(conn: DBConnection, user_id: UserID, collection_id: int):
    try:
        await crud.check_user_id(conn, user_id)
        await crud.check_collection_id(conn, user_id, collection_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    await crud.delete_collection(conn, collection_id)
    return Response(status_code=200)


@router.put("/{collection_id}", response_model=Collection)
async def update_collection(
        conn: DBConnection, user_id: UserID, collection_id: int, new_collection: CollectionCreate
) -> Collection:
    try:
        await crud.check_user_id(conn, user_id)
        await crud.check_collection_id(conn, user_id, collection_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    return await crud.update_collection(conn, collection_id, new_collection)



@router.get("/{collection_id}/cards", response_model=list[Card])
async def read_collection_cards(
        conn: DBConnection, user_id: UserID, collection_id: int
) -> list[Card]:
    try:
        await crud.check_user_id(conn, user_id)
        await crud.check_collection_id(conn, user_id, collection_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    return await crud.get_user_collection_cards(conn, user_id, collection_id)
