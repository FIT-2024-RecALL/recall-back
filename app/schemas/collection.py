from pydantic import BaseModel, Field

__all__ = ["Collection", "CollectionCreate"]


class CollectionCreate(BaseModel):
    title: str = Field(max_length=100)
    description: str | None = None


class Collection(CollectionCreate):
    id: int
    owner_id: int
