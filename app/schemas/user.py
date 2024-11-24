from pydantic import BaseModel, Field, EmailStr

__all__ = ["User", "UserAuth", "UserBase", "UserCreate"]


class UserBase(BaseModel):
    nickname: str = Field(max_length=50)
    email: EmailStr


class UserCreate(UserBase):
    password: str = Field(min_length=13, max_length=64)


class User(UserBase):
    id: int


class UserAuth(BaseModel):
    email: EmailStr
    password: str = Field(min_length=13, max_length=64)
