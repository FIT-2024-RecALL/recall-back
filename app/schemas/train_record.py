from pydantic import BaseModel

__all__ = ["TrainRecord", "TrainRecordCreate"]


class TrainRecordCreate(BaseModel):
    meta_data: str


class TrainRecord(TrainRecordCreate):
    id: int
    card_id: int
    user_id: int
