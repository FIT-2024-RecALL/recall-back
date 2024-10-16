from pydantic import BaseModel, Field


class CollectionBase(BaseModel):
    title: str = Field(max_length=100)
    description: str | None = None


class CollectionCreate(CollectionBase):
    pass


class Collection(CollectionBase):
    id: int
    owner_id: int

    class Config:
        orm_mode = True
