from datetime import datetime, timedelta, timezone

from fastapi import Request, HTTPException
from jose import jwt, JWTError
from passlib.context import CryptContext

from app.config import settings


__pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password: str) -> str:
    return __pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return __pwd_context.verify(plain_password, hashed_password)


def create_access_token(user_id: int) -> str:
    expire = datetime.now(timezone.utc) + timedelta(minutes=50)
    token_data = {"sub": str(user_id), "exp": expire}
    return jwt.encode(
        token_data,
        key=settings.auth_secret_key.get_secret_value(),
        algorithm=settings.auth_algorithm
    )


def get_token(request: Request) -> str:
    token = request.cookies.get("users_access_token")
    if not token:
        raise HTTPException(status_code=401, detail="Token not found")
    return token


def get_profile_id(token: str) -> int:
    try:
        payload = jwt.decode(
            token,
            key=settings.auth_secret_key.get_secret_value(),
            algorithms=settings.auth_algorithm
        )
    except JWTError:
        raise ValueError("Invalid or expired token")

    user_id = payload.get('sub')
    if not user_id:
        raise ValueError("User ID is undefined")
    return int(user_id)