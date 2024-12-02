from fastapi import APIRouter, HTTPException, Response

from app import crud, DBConnection, UserID, create_access_token
from app.schemas import User, UserAuth, UserBase, UserCreate, Card, Collection
from app.config import _settings


router = APIRouter(
    prefix="/user",
    tags=["user"]
)


@router.get("/profile", response_model=User)
async def read_user(conn: DBConnection, user_id: UserID) -> User:
    try:
        await crud.check_user_id(conn, user_id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    return await crud.get_user(conn, user_id)


@router.post("/register", response_model=User)
async def create_user(
        conn: DBConnection, response: Response, user: UserCreate, auto_login: bool = True
) -> User:
    users_with_data: list[int] = await crud.find_users_by_data(conn, user)
    if len(users_with_data) > 0:
        raise HTTPException(status_code=400, detail="Email or Nickname already registered")
    new_user: User = await crud.create_user(conn, user)
    if auto_login:
        access_token = create_access_token(new_user.id)
        response.set_cookie(
            key=_settings.access_token_key, value=access_token,
            **_settings.cookie_kwargs.model_dump()
        )
    return new_user


@router.put("/edit_profile", response_model=User)
async def update_user(conn: DBConnection, user_id: UserID, user: UserBase) -> User:
    users_with_data: list[int] = await crud.find_users_by_data(conn, user)
    if len(users_with_data) == 1 and users_with_data[0] != user_id or len(users_with_data) > 1:
        raise HTTPException(status_code=400, detail="Email or Nickname already registered")
    return await crud.update_user(conn, user_id, user)


@router.post("/login", response_model=User)
async def authenticate_user(conn: DBConnection, response: Response, user_data: UserAuth) -> User:
    try:
        user = await crud.authenticate_user(conn, user_data)
    except ValueError as e:
        raise HTTPException(status_code=401, detail=str(e))

    access_token = create_access_token(user.id)
    response.set_cookie(
        key=_settings.access_token_key, value=access_token, **_settings.cookie_kwargs.model_dump()
    )
    return user


@router.get("/cards", response_model=list[Card])
async def read_cards(
        conn: DBConnection, user_id: UserID, skip: int = 0, limit: int | None = None
) -> list[Card]:
    try:
        await crud.check_user_id(conn, user_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    return await crud.get_user_cards(conn, user_id, limit=limit, skip=skip)


@router.get("/collections", response_model=list[Collection])
async def read_collections(
        conn: DBConnection, user_id: UserID, skip: int = 0, limit: int | None = None
) -> list[Collection]:
    try:
        await crud.check_user_id(conn, user_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    return await crud.get_user_collections(conn, user_id, limit=limit, skip=skip)


@router.post("/logout", response_class=Response)
async def logout_user(response: Response) -> None:
    response.delete_cookie(key=_settings.access_token_key, **_settings.cookie_kwargs.model_dump())
    response.status_code = 200
    return


@router.delete("/delete_profile", response_class=Response)
async def delete_user(conn: DBConnection, user_id: UserID, response: Response) -> None:
    try:
        await crud.check_user_id(conn, user_id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    await crud.delete_user(conn, user_id)
    await logout_user(response)
