from abc import ABC, abstractmethod
from sqlalchemy import Table


class BaseRepository(ABC):
    @abstractmethod
    async def create(self):
        raise NotImplementedError

    @abstractmethod
    async def get_by_id(self):
        raise NotImplementedError

    @abstractmethod
    async def get_all(self):
        raise NotImplementedError

    @abstractmethod
    async def update(self):
        raise NotImplementedError

    @abstractmethod
    async def delete(self):
        raise NotImplementedError

    @abstractmethod
    async def exists(self):
        raise NotImplementedError


class SQLAlchemyRepository(BaseRepository):
    table: Table = ...

    async def create(self):
        #####
        result = await conn.execute(
            insert(CardTable).values(owner_id=user_id, **card.model_dump())
            .returning(CardTable.c[*Card.model_fields])
        )
        await conn.commit()
        return Card(**result.mappings().first())
        #####
        query = insert(UserTable).values(
            email=user.email, nickname=user.nickname, hashed_password=get_password_hash(user.password)
        ).returning(UserTable.c[*User.model_fields])
        result = await conn.execute(query)
        await conn.commit()
        return User(**result.mappings().first())
