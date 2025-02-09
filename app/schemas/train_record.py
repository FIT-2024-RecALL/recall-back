from datetime import datetime
from pydantic import Field

from .base import CamelCaseBaseModel


__all__ = ["TrainRecord", "TrainRecordCreate"]


class TrainRecordCreate(CamelCaseBaseModel):
    mark: int = Field(ge=1, le=5)


class TrainRecord(TrainRecordCreate):
    id: int
    card_id: int
    user_id: int
    repeat_date: datetime
    next_repeat_date: datetime
    progress: float = Field(ge=0.0, le=1.0)
