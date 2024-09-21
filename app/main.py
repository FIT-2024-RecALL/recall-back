from fastapi import FastAPI
from pydantic import BaseModel

import os
import utils


class Item(BaseModel):
    secret_text: str
    password: str

class Password(BaseModel):
    password: str


app = FastAPI()


data_base = [
    {
        "secret_key": "niera7arti",
        "secret_text": "Blah, blah\nBlah, blah, blah...",
        "password": "123veryGoodPassword"
    },
    {
        "secret_key": "oc_tene0egoo",
        "secret_text": "Some text here. Foo, bar. And so on...",
        "password": "kirill2002"
    }
]


@app.get("/secret")
async def check_secret():
    return {"secret": "very secret"}

@app.get("/secrets/{secret_key}")
async def take_secret(secret_key: str, password: Password):
    if data_base:
        for secret in data_base:
            if secret["secret_key"] == secret_key and secret["password"] == password.password:
                return utils.encrypt_text(secret["secret_text"])

@app.post("/generate")
async def create_secret(item: Item):
    pass
