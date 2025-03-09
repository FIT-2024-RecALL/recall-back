from fastapi import HTTPException

from app.core import get_password_hash, verify_password
from app.db import UnitOfWork
from app.repositories import UserRepository
from app.schemas import User, UserAuth, UserBase, UserCreate, UserDTO


__all__ = ["UserService"]


class UserService:
    def __init__(self):
        self.uow = UnitOfWork()

    async def register_user(self, user: UserCreate) -> User:
        async with self.uow.begin():
            user_repo = self.uow.get_repository(UserRepository)
            register_data = UserDTO(**user.model_dump()).table_dict()
            if len(await user_repo.find_users_by_creds(register_data)) > 0:
                raise HTTPException(status_code=400)  ## ТУТ ДОЛЖНО БЫТЬ КАСТОМНОЕ ИСКЛЮЧЕНИЕ!
            register_data["hashed_password"] = get_password_hash(register_data["hashed_password"])
            return await user_repo.create(register_data, User)

    async def get_user(self, user_id: int) -> User:
        async with self.uow.begin():
            user_repo = self.uow.get_repository(UserRepository)
            is_user_in_db = user_repo.table.c.id == user_id
            if not await user_repo.exists(is_user_in_db):
                raise HTTPException(status_code=400)  ## ТУТ ДОЛЖНО БЫТЬ КАСТОМНОЕ ИСКЛЮЧЕНИЕ!
            return await user_repo.get_one_or_none(is_user_in_db, User)

    async def update_profile(self, user_id: int, user_data: UserBase) -> User:
        async with (self.uow.begin()):
            user_repo = self.uow.get_repository(UserRepository)
            update_values = user_data.model_dump()
            users_with_data = await user_repo.find_users_by_creds(update_values)
            if len(users_with_data) == 1 and users_with_data[0] != user_id or len(users_with_data) > 1:
                raise HTTPException(status_code=400)  ## ТУТ ДОЛЖНО БЫТЬ КАСТОМНОЕ ИСКЛЮЧЕНИЕ!
            return await user_repo.update_one(user_repo.table.c.id == user_id, update_values, User)

    async def delete_profile(self, user_id: int) -> None:
        async with self.uow.begin():
            user_repo = self.uow.get_repository(UserRepository)
            is_user_in_db = user_repo.table.c.id == user_id
            if not await user_repo.exists(is_user_in_db):
                raise HTTPException(status_code=400)  ## ТУТ ДОЛЖНО БЫТЬ КАСТОМНОЕ ИСКЛЮЧЕНИЕ!
            await user_repo.delete(is_user_in_db)

    async def authenticate_user(self, user_data: UserAuth):
        async with self.uow.begin():
            user_repo = self.uow.get_repository(UserRepository)
            auth_data = UserDTO(email=user_data.email).table_dict()
            user = await user_repo.get_user_by_columns(auth_data, UserDTO)
            if user is None or not verify_password(user_data.password, user.password):
                raise HTTPException(status_code=400)  ## ТУТ ДОЛЖНО БЫТЬ КАСТОМНОЕ ИСКЛЮЧЕНИЕ!
            return User(**user.model_dump())
