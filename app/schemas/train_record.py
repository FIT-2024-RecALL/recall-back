from .base import CamelCaseBaseModel

__all__ = ["TrainRecord", "TrainRecordCreate"]


class TrainRecordCreate(CamelCaseBaseModel):
    meta_data: str


class TrainRecord(TrainRecordCreate):
    id: int
    card_id: int
    user_id: int
