from fastapi import APIRouter, HTTPException

from app import crud, schemas
from app.dependencies import DBConnection


router = APIRouter(
    prefix="/users",
    tags=["user"]
)


@router.get("/{user_id}", response_model=schemas.user.User)
def read_user(conn: DBConnection, user_id: int):
    user = crud.user.get_user(conn, user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.get("/", response_model=list[schemas.user.User])
def read_users(conn: DBConnection, limit: int = 100, skip: int = 0):
    return crud.user.get_users(conn, limit=limit, skip=skip)


@router.post("/", response_model=schemas.user.User)
def create_user(conn: DBConnection, user: schemas.user.UserCreate):
    try:
        created_user = crud.user.create_user(conn, user)
        return created_user
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/profile", response_model=schemas.user.User, tags=["profile"])
def read_current_user_profile(conn: DBConnection):
    pass
