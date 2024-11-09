from pydantic import BaseModel


class CardCreate(BaseModel):
    front_side: str
    back_side: str

class Card(CardCreate):
    id: int
