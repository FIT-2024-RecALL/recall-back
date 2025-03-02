from fastapi import HTTPException

from app.core import get_password_hash, verify_password, UserIdDep
from app.db.unit_of_work import UnitOfWork
from app.repositories import UserRepository
from app.schemas import User, UserAuth, UserCreate, UserDTO


class UserService:
    def __init__(self):
        self.uow = UnitOfWork()

    async def register_user(self, user: UserCreate) -> User:
        async with self.uow.begin():
            user_repo = self.uow.get_repository(UserRepository)
            register_data = UserDTO(**user.model_dump()).table_dict()
            if len(await user_repo.find_users_by_data(register_data)) > 0:
                raise HTTPException(status_code=400)  ## ТУТ ДОЛЖНО БЫТЬ КАСТОМНОЕ ИСКЛЮЧЕНИЕ!
            register_data["hashed_password"] = get_password_hash(register_data["hashed_password"])
            return await user_repo.create(register_data, User)

    async def get_user(self, user_id: UserIdDep):
        async with self.uow.begin():
            user_repo = self.uow.get_repository(UserRepository)
            exists_user_id = user_repo.table.c.id == user_id
            if not await user_repo.exists(exists_user_id):
                raise HTTPException(status_code=400)  ## ТУТ ДОЛЖНО БЫТЬ КАСТОМНОЕ ИСКЛЮЧЕНИЕ!
            return await user_repo.get_one_or_none(exists_user_id, User)

"""       
# nothing
async def check_user_id(conn: AsyncConnection, user_id: int) -> None:
    result = await conn.execute(select(exists().where(UserTable.c.id == user_id)))
    if not result.scalar():
        raise ValueError("User not found")

#CRUD
async def authenticate_user(conn: AsyncConnection, user_data: UserAuth) -> User:
    user = await get_user_by_email(conn, user_data.email)
    if user is None or not verify_password(user_data.password, user["hashed_password"]):
        raise ValueError("Entered email or password is not correct")
    return User(**user)
"""
