from contextlib import asynccontextmanager
from sqlalchemy.ext.asyncio import AsyncConnection
from typing import Type, TypeVar

from app.repositories import SQLAlchemyRepository

from .database import get_db_engine


__all__ = ["UnitOfWork"]


RepositoryType = TypeVar("RepositoryType", bound=SQLAlchemyRepository)


class UnitOfWork:
    """
    Класс реализующий паттерн Unit-Of-Work. Нужен для управления транзакциями при взаимодействии
    с базой данных.

    Этот класс обеспечивает выполнение ряда операций с базой данных в рамках одной транзакции,
    предоставляя методы для начала транзакции и инициализации репозиториев при установленном
    соединении.

    Attributes:
        connection (AsyncConnection | None): The active database connection, if any.
    """

    def __init__(self):
        self.connection: AsyncConnection | None = None

    @asynccontextmanager
    async def begin(self):
        async with get_db_engine().begin() as conn:
            self.connection = conn
            try:
                yield self
            except Exception:
                ## logging
                self.connection.rollback()
                raise
            finally:
                self.connection = None

    def get_repository(self, repo_class: Type[RepositoryType]) -> RepositoryType:
        if self.connection is None:
            raise RuntimeError("Connection is not established. Use 'async with uow.begin()'.")
        return repo_class(self.connection)
