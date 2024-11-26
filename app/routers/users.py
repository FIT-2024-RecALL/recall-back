from fastapi import APIRouter, HTTPException, Response

from app import crud, DBConnection, UserID, create_access_token
from app.schemas import User, UserAuth, UserBase, UserCreate
from app.config import _settings


router = APIRouter(
    prefix="/users",
    tags=["user"]
)


@router.get("/profile", response_model=User)
async def read_user(conn: DBConnection, user_id: UserID) -> User:
    return await crud.get_user(conn, user_id)


@router.post("/register", response_model=User)
async def create_user(conn: DBConnection, user: UserCreate) -> User:
    user_data = await crud.find_user_by_data(conn, user)
    if user_data is not None:
        raise HTTPException(status_code=400, detail="Email or Nickname already registered")
    return await crud.create_user(conn, user)


@router.put("/edit_profile", response_model=User)
async def update_user(conn: DBConnection, user_id: UserID, user: UserBase) -> User:
    user_data = await crud.find_user_by_data(conn, user)
    if user_data is not None and user_data["id"] != user_id:
        raise HTTPException(status_code=400, detail="Email or Nickname already registered")
    return await crud.update_user(conn, user_id, user)


@router.post("/login", response_class=Response)
async def authenticate_user(conn: DBConnection, response: Response, user_data: UserAuth) -> None:
    try:
        check_user_id = await crud.authenticate_user(conn, user_data)
    except ValueError as e:
        raise HTTPException(status_code=401, detail=str(e))

    access_token = create_access_token(check_user_id)
    response.set_cookie(
        key=_settings.access_token_key, value=access_token, **_settings.cookie_kwargs.model_dump()
    )
    response.status_code = 200
    return


@router.post("/logout", response_class=Response)
async def logout_user(response: Response) -> None:
    response.delete_cookie(key=_settings.access_token_key, **_settings.cookie_kwargs.model_dump())
    response.status_code = 200
    return


@router.delete("/delete_profile", response_class=Response)
async def delete_user(conn: DBConnection, user_id: UserID, response: Response) -> None:
    await crud.delete_user(conn, user_id)
    await logout_user(response)
