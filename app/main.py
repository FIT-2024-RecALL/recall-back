from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

import os
import utils


class SecretScheme(BaseModel):
    secret_text: str
    password: str


app = FastAPI()

allowed_hosts = ["http://localhost:5173"]
app.add_middleware(
    CORSMiddleware,
    allow_origins = allowed_hosts,
    allow_methods = ["*"],
    allow_headers = ["*"]
)

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


@app.get("/secrets/{secret_key}")
async def take_secret(secret_key: str, password: str):
    if data_base:
        for secret in data_base:
            if secret["secret_key"] == secret_key and secret["password"] == password:
                return utils.encrypt_text(secret["secret_text"])


@app.post("/generate")
async def create_secret(secret: SecretScheme):
    generated_secret_key: str = utils.generate_secrete_key()
    data_base.append({
        "secret_key": generated_secret_key,
        "secret_text": secret.secret_text,
        "password": secret.password
    })
    return generated_secret_key
