from pydantic import Field, EmailStr

from .base import CamelCaseBaseModel


__all__ = ["User", "UserAuth", "UserBase", "UserCreate"]


class UserBase(CamelCaseBaseModel):
    nickname: str = Field(min_length=1, max_length=35)
    email: EmailStr


class UserCreate(UserBase):
    password: str = Field(min_length=8, max_length=40)


class User(UserBase):
    id: int


class UserAuth(CamelCaseBaseModel):
    email: EmailStr
    password: str = Field(min_length=8, max_length=40)
