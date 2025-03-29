from pydantic import EmailStr, Field

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
    nickname: str | None = None
    password: str | None = Field(None, alias="hashed_password")

    @classmethod
    def fields(cls) -> list[str]:
        mapping = {"password": "hashed_password"}
        result_fields = super().fields()
        for field, alias in mapping.items():
            result_fields.remove(field)
            result_fields.append(alias)
        return result_fields

    def table_dict(self):
        return self.model_dump(exclude_unset=True, by_alias=True)
