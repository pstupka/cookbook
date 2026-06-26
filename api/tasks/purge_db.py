from sqlalchemy import text

from app.db.schema import SessionLocal

db = SessionLocal()

try:
    db.execute(text("DROP SCHEMA public CASCADE; CREATE SCHEMA public;"))
    db.commit()
    print("Purge completed successfully.")
finally:
    db.close()
