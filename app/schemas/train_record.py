from datetime import datetime

from pydantic import BaseModel, Field

__all__ = ["TrainRecord", "TrainRecordCreate"]


class TrainRecordCreate(BaseModel):
    mark: int = Field(ge=1, le=5)


class TrainRecord(BaseModel):
    id: int
    card_id: int
    user_id: int
    repeat_date: datetime
    next_repeat_date: datetime
    progress: float = Field(ge=0.0, le=1.0)
