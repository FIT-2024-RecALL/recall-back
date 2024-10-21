from pydantic import BaseModel, ConfigDict

from .train_record import TrainRecord


class CardCreate(BaseModel):
    content: str


class Card(CardCreate):
    model_config = ConfigDict(from_attributes=True)

    id: int
    train_records: list[TrainRecord] = []
