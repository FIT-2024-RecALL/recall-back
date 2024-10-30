from pydantic import BaseModel, Field


class CollectionCreate(BaseModel):
    title: str = Field(max_length=100)
    description: str | None = None


class Collection(CollectionCreate):
    id: int
    owner_id: int
