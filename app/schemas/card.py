from pydantic import BaseModel

__all__ = ["Card", "CardCreate"]


class CardCreate(BaseModel):
    front_side: str
    back_side: str


class Card(CardCreate):
    id: int
    owner_id: int
