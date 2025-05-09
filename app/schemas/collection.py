from pydantic import Field

from .base import CamelCaseBaseModel, PublicStatusMixin


__all__ = ["Collection", "CollectionCreate", "CollectionShort"]


class CollectionCreate(CamelCaseBaseModel):
    title: str = Field(min_length=1, max_length=100)
    description: str | None = None


class Collection(CollectionCreate, PublicStatusMixin):
    owner_id: int


class CollectionShort(PublicStatusMixin):
    owner_id: int
    title: str = Field(min_length=1, max_length=100)
