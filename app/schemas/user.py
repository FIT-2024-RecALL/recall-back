from pydantic import BaseModel, ConfigDict, Field

from .collection import Collection
from .train_record import TrainRecord


class UserBase(BaseModel):
    email: str
    nickname: str = Field(max_length=50)


class UserCreate(UserBase):
    password: str = Field(min_length=13, max_length=128)


class User(UserBase):
    id: int
