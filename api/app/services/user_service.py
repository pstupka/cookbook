from sqlalchemy.orm import Session

from app.core.security import hash_password
from app.db.schema import User


class UserService:
    def __init__(self, session: Session):
        self._db = session

    def list_users(self) -> list[User]:
        return self._db.query(User).all()

    def get_user(self, user_id: int) -> User | None:
        return self._db.query(User).filter(User.id == user_id).first()

    def get_by_username(self, username: str) -> User | None:
        return self._db.query(User).filter(User.username == username).first()

    def create_user(
        self,
        username: str,
        password: str,
        email: str | None = None,
        full_name: str | None = None,
        is_admin: bool = False,
    ) -> User:
        user = User(
            username=username,
            hashed_password=hash_password(password),
            email=email,
            full_name=full_name,
            is_admin=is_admin,
        )
        self._db.add(user)
        self._db.commit()
        self._db.refresh(user)
        return user

    def update_user(
        self,
        user_id: int,
        username: str | None = None,
        password: str | None = None,
        email: str | None = None,
        full_name: str | None = None,
    ) -> User | None:
        user = self.get_user(user_id)
        if not user:
            return None
        if username is not None:
            user.username = username
        if password is not None:
            user.hashed_password = hash_password(password)
        if email is not None:
            user.email = email
        if full_name is not None:
            user.full_name = full_name
        self._db.commit()
        self._db.refresh(user)
        return user

    def delete_user(self, user_id: int) -> bool:
        user = self.get_user(user_id)
        if not user:
            return False
        self._db.delete(user)
        self._db.commit()
        return True
