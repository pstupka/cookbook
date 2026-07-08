import logging

from app.db.schema import SessionLocal, User
from app.services.user_service import UserService

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def init_admin() -> User | None:
    db = SessionLocal()
    try:
        service = UserService(db)
        user = service.get_by_username("admin")
        if user:
            logger.info("Admin user already exists, skipping.")
            return user
        else:
            return service.create_user(
                username="admin",
                password="admin",
                email="admin@example.com",
                full_name="Admin User",
                is_admin=True,
            )
    finally:
        db.close()


if __name__ == "__main__":
    init_admin()
