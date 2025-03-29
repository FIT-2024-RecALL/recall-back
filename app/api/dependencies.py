from typing import Annotated, Optional
from fastapi import Depends, Body

from app.core import get_profile_id, get_profile_id_soft
from app.services import CardService, UserService, CollectionService, TrainRecordService


__all__ = [
    "CardServiceDep", "CollectionServiceDep", "TrainRecordServiceDep", 
    "UserIdDep", "UserIdSoftDep",
    "UserServiceDep", "IntListBody"
]


UserIdDep = Annotated[int, Depends(get_profile_id)]
UserIdSoftDep = Annotated[Optional[int], Depends(get_profile_id_soft)]
UserServiceDep = Annotated[UserService, Depends()]
CardServiceDep = Annotated[CardService, Depends()]
CollectionServiceDep = Annotated[CollectionService, Depends()]
TrainRecordServiceDep = Annotated[TrainRecordService, Depends()]

IntListBody = Annotated[list[int], Body(min_length=1, max_length=100)]
