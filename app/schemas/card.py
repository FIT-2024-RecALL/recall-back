from pydantic import BaseModel


class CardCreate(BaseModel):
    content: str


class Card(CardCreate):
    id: int
    train_record_id: int | None

    class Config:
        orm_mode = True
