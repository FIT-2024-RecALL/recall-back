from fastapi import APIRouter, HTTPException, Response

from app import auth
from app import crud
from app.dependencies import DBConnection
from app.schemas.user import User, UserAuth, UserCreate


router = APIRouter(
    prefix="/users",
    tags=["user"]
)


@router.get("/{user_id}", response_model=User)
async def read_user(conn: DBConnection, user_id: int):
    user = await crud.user.get_user(conn, user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.get("/", response_model=list[User])
async def read_users(conn: DBConnection, limit: int = 100, skip: int = 0):
    return await crud.user.get_users(conn, limit=limit, skip=skip)


@router.post("/register", response_model=User)
async def create_user(conn: DBConnection, user: UserCreate):
    try:
        return await crud.user.create_user(conn, user)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/login")
async def authenticate_user(conn: DBConnection, response: Response, user_data: UserAuth):
    try:
        check_user_id = await crud.user.authenticate_user(conn, user_data)
    except ValueError as e:
        raise HTTPException(status_code=401, detail=str(e))

    access_token = auth.utils.create_access_token({"sub": str(check_user_id)})
    response.set_cookie(key="users_access_token", value=access_token, httponly=True)
    return {"access_token": access_token, "refresh_token": None}


@router.get("/profile", response_model=User, tags=["profile"])
async def read_current_user_profile(conn: DBConnection):
    pass
