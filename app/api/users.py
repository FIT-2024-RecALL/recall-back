from fastapi import APIRouter, Response

from app.core import delete_cookie, UserIdDep, UserServiceDep, set_authentication_cookie
from app.schemas import User, UserAuth, UserBase, UserCreate, CollectionShort


router = APIRouter(
    prefix="/user",
    tags=["user"]
)


@router.get("/profile", response_model=User)
async def read_user(user_id: UserIdDep, user_service: UserServiceDep) -> User:
    return await user_service.get_user(user_id)


@router.post("/register", response_model=User)
async def create_user(
        response: Response, user: UserCreate, user_service: UserServiceDep, auto_login: bool = True
) -> User:
    new_user = await user_service.register_user(user)
    if auto_login:
        set_authentication_cookie(response, new_user.id)
    return new_user


@router.put("/edit_profile", response_model=User)
async def update_user(user_id: UserIdDep, user: UserBase, user_service: UserServiceDep) -> User:
    return await user_service.update_profile(user_id, user)


@router.delete("/delete_profile", response_class=Response)
async def delete_user(
        response: Response, user_id: UserIdDep, user_service: UserServiceDep
) -> None:
    await user_service.delete_profile(user_id)
    delete_cookie(response)


@router.post("/login", response_model=User)
async def authenticate_user(
        response: Response, user_data: UserAuth, user_service: UserServiceDep
) -> User:
    user = await user_service.authenticate_user(user_data)
    set_authentication_cookie(response, user.id)
    return user


@router.post("/logout")
async def logout_user(response: Response) -> None:
    delete_cookie(response)

"""
@router.get("/cards", response_model=list[int])
async def read_cards(
        conn: DBConnection, user_id: UserID, skip: int = 0, limit: int | None = None
) -> list[int]:
    try:
        await repositories.check_user_id(conn, user_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    return await repositories.get_user_cards(conn, user_id, limit=limit, skip=skip)


@router.get("/collections", response_model=list[CollectionShort])
async def read_collections(
        conn: DBConnection, user_id: UserID, skip: int = 0, limit: int | None = None
) -> list[CollectionShort]:
    try:
        await repositories.check_user_id(conn, user_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    return await repositories.get_user_collections_short(conn, user_id, limit=limit, skip=skip)
"""