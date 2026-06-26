from datetime import datetime, timedelta, timezone

import jwt
from pwdlib import PasswordHash

from app.core.config import config

password_hash = PasswordHash.recommended()
DUMMY_HASH = password_hash.hash("dummypassword")  # timing-attack mitigation


def verify_password(plain: str, hashed: str) -> bool:
    return password_hash.verify(plain, hashed)


def hash_password(plain: str) -> str:
    return password_hash.hash(plain)


def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + (
        expires_delta or timedelta(minutes=config.api_access_token_expire_minutes)
    )
    to_encode["exp"] = expire
    return jwt.encode(to_encode, config.api_secret_key, algorithm=config.api_algorithm)
