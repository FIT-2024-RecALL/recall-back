from pydantic import Field

from .base import CamelCaseBaseModel, IsPublicModelMixin


__all__ = ["Card", "CardCreate"]


class CardCreate(CamelCaseBaseModel):
    front_side: str = Field(min_length=1)
    back_side: str = Field(min_length=1)


class Card(CardCreate, IsPublicModelMixin):
    id: int
    owner_id: int
