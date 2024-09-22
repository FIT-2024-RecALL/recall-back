from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

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

data_base: list[dict[str, str]] = [
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
async def take_secret(secret_key: str, password: str) -> dict[str, str] | dict[str, None]:
    if data_base:
        for secret_id, secret in enumerate(data_base):
            if (secret["secret_key"] == secret_key and
                    utils.decrypt_text(secret["password"]) == password):
                secret_text: str = utils.encrypt_text(secret["secret_text"])
                data_base.pop(secret_id)
                return {"secret_text": secret_text}
    return {"secret_text": None}


@app.post("/generate")
async def create_secret(secret: SecretScheme) -> dict[str, str]:
    generated_secret_key: str = utils.generate_secrete_key()
    data_base.append({
        "secret_key": generated_secret_key,
        "secret_text": utils.encrypt_text(secret.secret_text),
        "password": utils.encrypt_text(secret.password)
    })
    return {"secret_key": generated_secret_key}
