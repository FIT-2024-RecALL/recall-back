from pydantic import BaseModel, ConfigDict, Field

from .collection import Collection
from .train_record import TrainRecord


class UserBase(BaseModel):
    email: str
    name: str = Field(max_length=50)


class UserCreate(UserBase):
    password: str = Field(min_length=13, max_length=50)


class User(UserBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    collections: list[Collection] = []
    train_records: list[TrainRecord] = []
