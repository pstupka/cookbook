import pytest

BASE_URL = "/api/v1/auth"
USER_URL = "/api/v1/users"


@pytest.fixture()
def registered_user(client):
    client.post(USER_URL, json={"username": "johndoe", "password": "secret"})


def test_login_success(client, registered_user):
    response = client.post(f"{BASE_URL}/token", data={"username": "johndoe", "password": "secret"})

    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"


def test_login_returns_jwt(client, registered_user):
    import jwt

    from app.core.config import config

    response = client.post(f"{BASE_URL}/token", data={"username": "johndoe", "password": "secret"})
    token = response.json()["access_token"]
    payload = jwt.decode(token, config.api_secret_key, algorithms=[config.api_algorithm])

    assert payload["sub"] == "johndoe"


def test_login_wrong_password(client, registered_user):
    response = client.post(f"{BASE_URL}/token", data={"username": "johndoe", "password": "wrong"})

    assert response.status_code == 401


def test_login_unknown_user(client):
    response = client.post(f"{BASE_URL}/token", data={"username": "nobody", "password": "secret"})

    assert response.status_code == 401


def test_login_missing_credentials(client):
    response = client.post(f"{BASE_URL}/token", data={})

    assert response.status_code == 422
