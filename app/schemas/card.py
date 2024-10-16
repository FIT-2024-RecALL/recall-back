from pydantic import BaseModel

from .train_record import TrainRecord


class CardCreate(BaseModel):
    content: str


class Card(CardCreate):
    id: int
    train_records: list[TrainRecord] = []

    class Config:
        orm_mode = True
