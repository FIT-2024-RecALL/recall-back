from datetime import datetime, timedelta, timezone

from fastapi import Depends, Request, HTTPException
from jose import jwt, JWTError
from passlib.context import CryptContext

from app.config import _settings

__all__ = ["get_password_hash", "verify_password", "get_expiration_datetime", "create_access_token", "get_profile_id"]

__pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password: str) -> str:
    return __pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return __pwd_context.verify(plain_password, hashed_password)


def get_expiration_datetime() -> datetime:
    return datetime.now(timezone.utc) + timedelta(hours=_settings.expire_hours)

def create_access_token(user_id: int) -> str:
    expire = get_expiration_datetime()
    token_data = {"sub": str(user_id), "exp": expire}
    return jwt.encode(
        token_data,
        key=_settings.auth_secret_key.get_secret_value(),
        algorithm=_settings.auth_algorithm
    )


def get_token(request: Request) -> str:
    token = request.cookies.get(_settings.access_token_key)
    if not token:
        raise HTTPException(status_code=401, detail="Token not found")
    return token


def get_profile_id(token: str = Depends(get_token)) -> int:
    try:
        payload = jwt.decode(
            token,
            key=_settings.auth_secret_key.get_secret_value(),
            algorithms=_settings.auth_algorithm
        )
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid or expired token")

    user_id = payload.get('sub')
    if not user_id:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
    return int(user_id)
