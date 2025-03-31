from typing import Annotated, Optional
from fastapi import Depends, Body

from app.core import get_profile_id, get_profile_id_soft
from app.services import CardService, UserService, CollectionService, TrainRecordService, StorageService


__all__ = [
    "CardServiceDep", "CollectionServiceDep", 
    "TrainRecordServiceDep", "StorageServiceDep",
    "UserIdDep", "UserIdSoftDep",
    "UserServiceDep", "IntListBody"
]


UserIdDep = Annotated[int, Depends(get_profile_id)]
UserIdSoftDep = Annotated[Optional[int], Depends(get_profile_id_soft)]
UserServiceDep = Annotated[UserService, Depends()]
CardServiceDep = Annotated[CardService, Depends()]
CollectionServiceDep = Annotated[CollectionService, Depends()]
TrainRecordServiceDep = Annotated[TrainRecordService, Depends()]
StorageServiceDep = Annotated[StorageService, Depends()]

IntListBody = Annotated[list[int], Body(min_length=1, max_length=100)]
