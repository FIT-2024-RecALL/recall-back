from typing import Annotated
from fastapi import Depends, Body

from app.core import get_profile_id


__all__ = ["UserIdDep", "IntListDep", "UserServiceDep"]

from app.services import UserService

UserIdDep = Annotated[int, Depends(get_profile_id)]
IntListDep = Annotated[list[int], Body(min_length=1, max_length=100)]

UserServiceDep = Annotated[UserService, Depends()]
