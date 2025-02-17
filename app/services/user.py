from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncConnection

from app.core import get_password_hash, verify_password
from app.db.unit_of_work import UnitOfWork
from app.repositories import UserRepository
from app.schemas import User, UserAuth, UserCreate, UserDTO


class UserService:
    def __init__(self):
        self.uow = UnitOfWork()

    async def create_user(self, user: UserCreate) -> User:
        async with self.uow.begin():
            user_repo: UserRepository = self.uow.get_repository(UserRepository)
            register_data = UserDTO(**user.model_dump()).table_dict()
            if len(await user_repo.find_users_by_data(register_data)) > 0:
                raise HTTPException(status_code=400)  ## ТУТ ДОЛЖНО БЫТЬ КАСТОМНОЕ ИСКЛЮЧЕНИЕ!
            register_data["hashed_password"] = get_password_hash(register_data["hashed_password"])
            return await user_repo.create(register_data, User)


#ROUTER
async def read_user(conn: DBConnection, user_id: UserID) -> User:
    try:
        await repositories.check_user_id(conn, user_id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    return await repositories.get_user(conn, user_id)

#CRUD
async def authenticate_user(conn: AsyncConnection, user_data: UserAuth) -> User:
    user = await get_user_by_email(conn, user_data.email)
    if user is None or not verify_password(user_data.password, user["hashed_password"]):
        raise ValueError("Entered email or password is not correct")
    return User(**user)
