from pydantic import Field, EmailStr

from .base import CamelCaseBaseModel

__all__ = ["User", "UserAuth", "UserBase", "UserCreate"]


class UserBase(CamelCaseBaseModel):
    nickname: str = Field(max_length=50)
    email: EmailStr


class UserCreate(UserBase):
    password: str = Field(min_length=8, max_length=64)


class User(UserBase):
    id: int


class UserAuth(CamelCaseBaseModel):
    email: EmailStr
    password: str = Field(min_length=13, max_length=64)
