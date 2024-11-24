from pydantic import BaseModel, Field

__all__ = ["Card", "CardCreate"]


class CardCreate(BaseModel):
    front_side: str = Field(min_length=1)
    back_side: str = Field(min_length=1)


class Card(CardCreate):
    id: int
    owner_id: int
