from typing import Optional
from datetime import datetime, timedelta, timezone
from fastapi import Depends, Request, HTTPException, Response
from jose import jwt, JWTError
from passlib.context import CryptContext

from .config import get_settings


__all__ = ["get_password_hash", "verify_password", "get_expiration_datetime", "delete_cookie",
           "create_access_token", "get_profile_id", "get_profile_id_soft", "set_authentication_cookie"]


__pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_password_hash(password: str) -> str:
    return __pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return __pwd_context.verify(plain_password, hashed_password)


def get_expiration_datetime() -> datetime:
    return datetime.now(timezone.utc) + timedelta(hours=get_settings().expire_hours)


def create_access_token(user_id: int) -> str:
    expire = get_expiration_datetime()
    token_data = {"sub": str(user_id), "exp": expire}
    return jwt.encode(
        token_data,
        key=get_settings().auth_secret_key.get_secret_value(),
        algorithm=get_settings().auth_algorithm
    )


def get_token(request: Request) -> str | None:
    token = request.cookies.get(get_settings().access_token_key)
    if not token:
        return None
    return token


def get_profile_id(token: str | None = Depends(get_token)) -> int:
    """Бросает исключение, если есть проблемы с токеном"""
    if not token:
        raise HTTPException(status_code=401, detail="This action requires authorization")
    try:
        payload = jwt.decode(
            token,
            key=get_settings().auth_secret_key.get_secret_value(),
            algorithms=get_settings().auth_algorithm
        )
    except JWTError:
        raise HTTPException(status_code=401, detail="Your authorization is expired")

    user_id = payload.get('sub')
    if not user_id:
        raise HTTPException(status_code=401, detail="Your authorization is expired")
    return int(user_id)


def get_profile_id_soft(token: str | None = Depends(get_token)) -> int | None:
    """Возвращает `None`, если есть проблемы с токеном"""
    try:
        return int(get_profile_id(token))
    except HTTPException:
        return None
    


def set_authentication_cookie(response: Response, user_id: int) -> None:
    response.set_cookie(
        key=get_settings().access_token_key,
        value=create_access_token(user_id),
        expires=get_expiration_datetime(),
        **get_settings().cookie_kwargs.model_dump()
    )


def delete_cookie(response: Response) -> None:
    response.delete_cookie(
        key=get_settings().access_token_key, **get_settings().cookie_kwargs.model_dump()
    )
