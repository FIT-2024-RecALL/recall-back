from pydantic import BaseModel, Field


class UserBase(BaseModel):
    nickname: str = Field(max_length=50)
    email: str

class UserCreate(UserBase):
    password: str = Field(min_length=13, max_length=128)

class User(UserBase):
    id: int

class UserAuth(BaseModel):
    email: str
    password: str = Field(min_length=13, max_length=128)
