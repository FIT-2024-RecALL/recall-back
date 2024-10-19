from pydantic import BaseModel, ConfigDict, Field

from .card import Card


class CollectionCreate(BaseModel):
    title: str = Field(max_length=100)
    description: str | None = None


class Collection(CollectionCreate):
    model_config = ConfigDict(from_attributes=True)

    id: int
    owner_id: int
    cards: list[Card] = []
