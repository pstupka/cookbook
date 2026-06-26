import os

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

os.environ.setdefault("DB_HOST", "localhost")
os.environ.setdefault("DB_PORT", "5432")
os.environ.setdefault("DB_USER", "test")
os.environ.setdefault("DB_PASSWORD", "test")
os.environ.setdefault("DB_NAME", "test")

from app.api.v1.routes.ingredients import get_ingredient_service
from app.api.v1.routes.recipes import get_recipe_service
from app.db.schema import Base
from app.main import app
from app.services.ingredient_service import IngredientService
from app.services.recipe_service import RecipeService


@pytest.fixture()
def db_session():
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    yield session
    session.close()
    Base.metadata.drop_all(engine)


@pytest.fixture()
def client(db_session):
    app.dependency_overrides[get_recipe_service] = lambda: RecipeService(session=db_session)
    app.dependency_overrides[get_ingredient_service] = lambda: IngredientService(session=db_session)
    with TestClient(app) as c:
        yield c
    app.dependency_overrides.clear()
