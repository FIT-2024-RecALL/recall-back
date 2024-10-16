from pydantic import BaseModel, Field

from .card import Card


class CollectionCreate(BaseModel):
    title: str = Field(max_length=100)
    description: str | None = None


class Collection(CollectionCreate):
    id: int
    owner_id: int
    cards: list[Card] = []

    class Config:
        orm_mode = True
