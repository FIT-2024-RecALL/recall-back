from pydantic import Field

from .base import CamelCaseBaseModel


__all__ = ["Card", "CardCreate"]


class CardCreate(CamelCaseBaseModel):
    front_side: str = Field(min_length=1)
    back_side: str = Field(min_length=1)


class Card(CardCreate):
    id: int
    owner_id: int
    is_public: bool
