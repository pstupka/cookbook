from fastapi import FastAPI

from app.api.v1.routes import ingredients, recipes, users
from app.core.config import config
from app.core.logging import setup_logging
from app.db.schema import Base, engine

setup_logging()
Base.metadata.create_all(bind=engine)

app = FastAPI(title=config.app_name)


# Register routes
app.include_router(users.router, prefix="/api/v1")
app.include_router(recipes.router, prefix="/api/v1")
app.include_router(ingredients.router, prefix="/api/v1")
