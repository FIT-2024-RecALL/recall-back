from pydantic import BaseModel, ConfigDict


class TrainRecordCreate(BaseModel):
    meta_data: str


class TrainRecord(TrainRecordCreate):
    model_config = ConfigDict(from_attributes=True)

    id: int
    card_id: int
    user_id: int
