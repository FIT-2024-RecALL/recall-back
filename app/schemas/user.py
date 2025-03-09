from pydantic import Field, EmailStr

from .base import CamelCaseBaseModel


__all__ = ["User", "UserAuth", "UserBase", "UserCreate", "UserDTO"]


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


class UserDTO(CamelCaseBaseModel):
    id: int | None = None
    email: EmailStr | None = None
    nickname: str | None = Field(None, min_length=1, max_length=35)
    password: str | None = Field(None, min_length=8, max_length=40)

    @classmethod
    def fields(cls) -> list[str]:
        return ["id", "email", "nickname", "hashed_password"]

    def table_dict(self):
        table_repr = dict()
        if self.id is not None: table_repr["id"] = self.id
        if self.email is not None: table_repr["email"] = self.email
        if self.nickname is not None: table_repr["nickname"] = self.nickname
        if self.password is not None: table_repr["hashed_password"] = self.password
        return table_repr
