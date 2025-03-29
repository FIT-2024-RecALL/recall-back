from contextlib import asynccontextmanager
from contextvars import ContextVar
from fastapi import Depends
from typing import Annotated, Type, TypeVar

from app.repositories import BaseSQLAlchemyRepository

from .database import get_db_engine


__all__ = ["UnitOfWork", "UnitOfWorkDep"]


RepositoryType = TypeVar("RepositoryType", bound=BaseSQLAlchemyRepository)


class UnitOfWork:
    """
    Класс реализующий паттерн Unit-Of-Work. Нужен для управления транзакциями при взаимодействии
    с базой данных.

    Этот класс обеспечивает выполнение ряда операций с базой данных в рамках одной транзакции,
    предоставляя методы для начала транзакции и инициализации репозиториев при установленном
    соединении.
    """
    __connection = ContextVar("connection", default=None)

    @asynccontextmanager
    async def begin(self):
        async with get_db_engine().begin() as conn:
            token = self.__connection.set(conn)
            try:
                yield self
            except Exception:
                ## logging
                raise  # Без возбуждения исключения нужен явный rollback соединения
            finally:
                self.__connection.reset(token)

    def get_repository(self, repo_class: Type[RepositoryType]) -> RepositoryType:
        current_connection = self.__connection.get()
        if current_connection is None:
            raise RuntimeError("Connection is not established. Use 'async with uow.begin()'.")
        return repo_class(current_connection)


UnitOfWorkDep = Annotated[UnitOfWork, Depends()]
