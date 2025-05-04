from pydantic import Field

from .base import CamelCaseBaseModel, IsPublicModelMixin, IsPublicIdModel


__all__ = ["Collection", "CollectionCreate", "CollectionShort"]


class CollectionCreate(CamelCaseBaseModel):
    title: str = Field(min_length=1, max_length=100)
    description: str | None = None


class Collection(CollectionCreate, IsPublicModelMixin):
    owner_id: int


class CollectionShort(IsPublicIdModel):
    owner_id: int
    title: str = Field(min_length=1, max_length=100)
