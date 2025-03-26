from typing import Annotated
from fastapi import Depends, Body

from app.core import get_profile_id
from app.db import UnitOfWork
from app.services import CardService, UserService


__all__ = ["CardServiceDep", "UserIdDep", "UnitOfWorkDep", "UserServiceDep", "IntListBody"]


UserIdDep = Annotated[int, Depends(get_profile_id)]
UnitOfWorkDep = Annotated[UnitOfWork, Depends()]
UserServiceDep = Annotated[UserService, Depends()]
CardServiceDep = Annotated[CardService, Depends()]

IntListBody = Annotated[list[int], Body(min_length=1, max_length=100)]
