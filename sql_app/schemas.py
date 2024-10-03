from pydantic import BaseModel, Field


class ItemBase(BaseModel):
    title: str = Field(
        title="The description of the item", min_length=6
    )
    description: str | None = None


class ItemCreate(ItemBase):
    pass


class Item(ItemBase):
    id: int
    owner_id: int

    class Config:
        orm_mode = True


class UserBase(BaseModel):
    email: str


class UserCreate(UserBase):
    password: str = Field(
        title="The description of the password properties", min_length=13, max_length=50
    )


class User(UserBase):
    id: int
    is_active: bool
    items: list[Item] = []

    class Config:
        orm_mode = True
