import pytest

from app.services.auth_service import AuthService
from app.services.user_service import UserService


@pytest.fixture()
def user_service(db_session):
    return UserService(session=db_session)


@pytest.fixture()
def auth_service(db_session):
    return AuthService(session=db_session)


@pytest.fixture()
def existing_user(user_service):
    return user_service.create_user("johndoe", "secret")


def test_authenticate_success(auth_service, existing_user):
    token = auth_service.authenticate("johndoe", "secret")

    assert isinstance(token, str)
    assert len(token) > 0


def test_authenticate_returns_valid_jwt(auth_service, existing_user):
    import jwt

    from app.core.config import config

    token = auth_service.authenticate("johndoe", "secret")
    payload = jwt.decode(token, config.api_secret_key, algorithms=[config.api_algorithm])

    assert payload["sub"] == "johndoe"
    assert "exp" in payload


def test_authenticate_wrong_password(auth_service, existing_user):
    with pytest.raises(ValueError, match="Incorrect username or password"):
        auth_service.authenticate("johndoe", "wrongpassword")


def test_authenticate_unknown_user(auth_service):
    with pytest.raises(ValueError, match="Incorrect username or password"):
        auth_service.authenticate("nobody", "secret")
