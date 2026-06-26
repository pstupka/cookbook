from datetime import timedelta

from sqlalchemy.orm import Session

from app.core.config import config
from app.core.security import DUMMY_HASH, create_access_token, verify_password
from app.db.schema import User as UserORM


class AuthService:
    def __init__(self, session: Session):
        self._db = session

    def authenticate(self, username: str, password: str) -> str:
        user = self._db.query(UserORM).filter(UserORM.username == username).first()
        if not user:
            verify_password(password, DUMMY_HASH)
            raise ValueError("Incorrect username or password")
        if not verify_password(password, user.hashed_password):
            raise ValueError("Incorrect username or password")
        return create_access_token(
            data={"sub": user.username},
            expires_delta=timedelta(minutes=config.api_access_token_expire_minutes),
        )
