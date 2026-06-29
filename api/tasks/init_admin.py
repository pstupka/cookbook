import logging

from app.db.schema import SessionLocal
from app.services.user_service import UserService

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

db = SessionLocal()
try:
    user = UserService(db).create_user(
        username="admin",
        password="admin",
        email="admin@example.com",
        full_name="Admin User",
        is_admin=True,
    )

    if user:
        logger.info("Admin user created.")
finally:
    db.close()
