from pydantic import BaseModel, Field


class TrainRecordBase(BaseModel):
    meta_data: str


class TrainRecordCreate(TrainRecordBase):
    pass


class TrainRecord(TrainRecordBase):
    id: int
    user_id: int

    class Config:
        orm_mode = True
