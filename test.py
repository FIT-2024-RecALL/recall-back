from pydantic import BaseModel

class Example(BaseModel):
    id: int | None = None
    email: str | None = None

class Check(BaseModel):
    email: str

a = Example(id=1, email="Sas")
b = Check(**a.model_dump())
print(b.model_dump())
c = Check(email="Lol", abobus=10342, kek=9, sis=True)
print(c)