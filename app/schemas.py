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


class UserBase(BaseModel):
    email: str
    name: str = Field(max_length=50)

class UserCreate(UserBase):
    password: str = Field(min_length=13, max_length=50)

class User(UserBase):
    id: int
    collections: list[Collection] = []

    class Config:
        orm_mode = True
