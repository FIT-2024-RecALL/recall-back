from fastapi import APIRouter, Response

from app.core import delete_cookie, set_authentication_cookie
from app.schemas import CollectionShort, User, UserAuth, UserBase, UserCreate

from .dependencies import UserIdDep, UnitOfWorkDep, UserServiceDep

router = APIRouter(
    prefix="/user",
    tags=["user"]
)


@router.get("/profile", response_model=User)
async def read_user(user_id: UserIdDep, user_service: UserServiceDep, uow: UnitOfWorkDep) -> User:
    return await user_service.get_user(uow, user_id)


@router.get("/collections", response_model=list[CollectionShort])
async def read_user_collections(
        user_id: UserIdDep, user_service: UserServiceDep, uow: UnitOfWorkDep,
        offset: int = 0, limit: int | None = None
) -> list[CollectionShort]:
    return await user_service.get_user_collections(uow, user_id, offset, limit)


@router.get("/cards", response_model=list[int])
async def read_user_cards(
        user_id: UserIdDep, user_service: UserServiceDep, uow: UnitOfWorkDep,
        skip: int = 0, limit: int | None = None
) -> list[int]:
    return await user_service.get_user_cards(uow, user_id, skip, limit)


@router.post("/register", response_model=User)
async def create_user(
        response: Response, user: UserCreate, user_service: UserServiceDep, uow: UnitOfWorkDep,
        auto_login: bool = True
) -> User:
    new_user = await user_service.register_user(uow, user)
    if auto_login:
        set_authentication_cookie(response, new_user.id)
    return new_user


@router.put("/edit_profile", response_model=User)
async def update_user(
        user_id: UserIdDep, user: UserBase, user_service: UserServiceDep, uow: UnitOfWorkDep
) -> User:
    return await user_service.update_profile(uow, user_id, user)


@router.delete("/delete_profile", response_class=Response)
async def delete_user(
        response: Response, user_id: UserIdDep, user_service: UserServiceDep, uow: UnitOfWorkDep
) -> None:
    await user_service.delete_profile(uow, user_id)
    delete_cookie(response)


@router.post("/login", response_model=User)
async def authenticate_user(
        response: Response, user_data: UserAuth, user_service: UserServiceDep, uow: UnitOfWorkDep
) -> User:
    user = await user_service.authenticate_user(uow, user_data)
    set_authentication_cookie(response, user.id)
    return user


@router.post("/logout")
async def logout_user(response: Response) -> None:
    delete_cookie(response)
