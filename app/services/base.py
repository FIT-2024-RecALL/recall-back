from abc import ABC

from app.db import UnitOfWorkDep


__all__ = ["BaseService", "with_unit_of_work"]


def with_unit_of_work(method):
    async def wrapper(self, *args, **kwargs):
        async with self.uow.begin():
            return await method(self, *args, **kwargs)
    return wrapper


class BaseService(ABC):
    def __init__(self, unit_of_work: UnitOfWorkDep):
        self.uow = unit_of_work
