from abc import ABC

from app.db import UnitOfWorkDep


__all__ = ["BaseService"]


class BaseService(ABC):
    def __init__(self, unit_of_work: UnitOfWorkDep):
        self.uow = unit_of_work
