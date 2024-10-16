from pydantic import BaseModel


class TrainRecordCreate(BaseModel):
    meta_data: str


class TrainRecord(TrainRecordCreate):
    id: int
    card_id: int
    user_id: int

    class Config:
        orm_mode = True
