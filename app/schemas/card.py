from pydantic import BaseModel


class CardCreate(BaseModel):
    content: str

class Card(CardCreate):
    id: int
