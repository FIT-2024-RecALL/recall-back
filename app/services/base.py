from abc import ABC
from fastapi import Depends
from typing import Annotated

from app.db import UnitOfWork


__all__ = ["BaseService", "UnitOfWorkDep"]


UnitOfWorkDep = Annotated[UnitOfWork, Depends()]


class BaseService(ABC):
    def __init__(self, unit_of_work: UnitOfWorkDep):
        self.uow = unit_of_work
