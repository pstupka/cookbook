from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.v1.routes import auth, ingredients, recipes, users
from app.core.config import config
from app.core.logging import setup_logging

setup_logging()

app = (
    FastAPI(docs_url=None, redoc_url=None, title=config.app_name)
    if not config.debug
    else FastAPI(title=config.app_name)
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=config.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register routes
app.include_router(auth.router, prefix="/api/v1")
app.include_router(users.router, prefix="/api/v1")
app.include_router(recipes.router, prefix="/api/v1")
app.include_router(ingredients.router, prefix="/api/v1")
