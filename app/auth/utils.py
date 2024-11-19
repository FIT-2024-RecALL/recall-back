from datetime import datetime, timedelta, timezone

from fastapi import Request, HTTPException
from jose import jwt
from passlib.context import CryptContext

from app.config import settings


__pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password: str) -> str:
    return __pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return __pwd_context.verify(plain_password, hashed_password)


def create_access_token(data: dict) -> str:
    to_encode: dict = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(days=30)
    to_encode.update({"exp": expire})
    auth_data: dict = settings.auth_data
    encode_jwt = jwt.encode(to_encode, auth_data["secret_key"], algorithm=auth_data["algorithm"])
    return encode_jwt


def get_token(request: Request) -> str:
    token = request.cookies.get("users_access_token")
    if not token:
        raise HTTPException(status_code=401, detail="Token not found")
    return token
