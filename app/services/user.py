from fastapi import HTTPException

from app.core import get_password_hash, verify_password
from app.db import UnitOfWork
from app.repositories import UserRepository
from app.schemas import User, UserAuth, UserBase, UserCreate, UserDTO


__all__ = ["UserService"]


class UserService:
    async def register_user(self, uow: UnitOfWork, user: UserCreate) -> User:
        async with uow.begin():
            user_repo = uow.get_repository(UserRepository)
            register_data = UserDTO(**user.model_dump()).table_dict()
            if len(await user_repo.find_users_by_creds(register_data)) > 0:
                raise HTTPException(status_code=400)  ## ТУТ ДОЛЖНО БЫТЬ КАСТОМНОЕ ИСКЛЮЧЕНИЕ!
            register_data["hashed_password"] = get_password_hash(register_data["hashed_password"])
            return await user_repo.create_one(register_data, User)

    async def get_user(self, uow: UnitOfWork, user_id: int) -> User:
        async with uow.begin():
            user = await uow.get_repository(UserRepository).get_user_by_id(user_id, User)
            if user is None:
                raise HTTPException(status_code=400)  ## ТУТ ДОЛЖНО БЫТЬ КАСТОМНОЕ ИСКЛЮЧЕНИЕ!
            return user

    async def update_profile(self, uow: UnitOfWork, user_id: int, user_data: UserBase) -> User:
        async with uow.begin():
            user_repo = uow.get_repository(UserRepository)
            update_values = user_data.model_dump()
            users_with_data = await user_repo.find_users_by_creds(update_values)
            if len(users_with_data) == 1 and users_with_data[0] != user_id or len(users_with_data) > 1:
                raise HTTPException(status_code=400)  ## ТУТ ДОЛЖНО БЫТЬ КАСТОМНОЕ ИСКЛЮЧЕНИЕ!
            return await user_repo.update_user_by_id(user_id, update_values, User)

    async def delete_profile(self, uow: UnitOfWork, user_id: int) -> None:
        async with uow.begin():
            user_repo = uow.get_repository(UserRepository)
            if not await user_repo.exists_user_with_id(user_id):
                raise HTTPException(status_code=400)  ## ТУТ ДОЛЖНО БЫТЬ КАСТОМНОЕ ИСКЛЮЧЕНИЕ!
            await user_repo.delete_user_by_id(user_id)

    async def authenticate_user(self, uow: UnitOfWork, user_data: UserAuth):
        async with uow.begin():
            auth_data = UserDTO(email=user_data.email).table_dict()
            user = await uow.get_repository(UserRepository).get_user_by_columns(auth_data, UserDTO)
            if user is None or not verify_password(user_data.password, user.password):
                raise HTTPException(status_code=400)  ## ТУТ ДОЛЖНО БЫТЬ КАСТОМНОЕ ИСКЛЮЧЕНИЕ!
            return User(**user.model_dump())
