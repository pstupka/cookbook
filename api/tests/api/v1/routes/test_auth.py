import pytest

BASE_URL = "/api/v1/auth"
REGISTER_URL = f"{BASE_URL}/register"
TOKEN_URL = f"{BASE_URL}/token"


@pytest.fixture()
def registered_user(client):
    client.post(REGISTER_URL, json={"username": "johndoe", "password": "secret"})


# --- Register ---


def test_register_success(client):
    response = client.post(REGISTER_URL, json={"username": "newuser", "password": "secret"})

    assert response.status_code == 201
    data = response.json()
    assert data["username"] == "newuser"
    assert data["is_admin"] is False


def test_register_with_optional_fields(client):
    response = client.post(
        REGISTER_URL,
        json={
            "username": "newuser",
            "password": "secret",
            "email": "new@example.com",
            "full_name": "New User",
        },
    )

    assert response.status_code == 201
    assert response.json()["email"] == "new@example.com"


def test_register_cannot_create_admin(client):
    response = client.post(
        REGISTER_URL, json={"username": "hacker", "password": "secret", "is_admin": True}
    )

    assert response.status_code == 201
    assert response.json()["is_admin"] is False


def test_register_duplicate_username(client):
    client.post(REGISTER_URL, json={"username": "johndoe", "password": "secret"})

    response = client.post(REGISTER_URL, json={"username": "johndoe", "password": "other"})

    assert response.status_code == 409


# --- Login ---


def test_login_success(client, registered_user):
    response = client.post(TOKEN_URL, data={"username": "johndoe", "password": "secret"})

    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"


def test_login_returns_jwt(client, registered_user):
    import jwt

    from app.core.config import config

    response = client.post(TOKEN_URL, data={"username": "johndoe", "password": "secret"})
    token = response.json()["access_token"]
    payload = jwt.decode(token, config.api_secret_key, algorithms=[config.api_algorithm])

    assert payload["sub"] == "johndoe"


def test_login_wrong_password(client, registered_user):
    assert (
        client.post(TOKEN_URL, data={"username": "johndoe", "password": "wrong"}).status_code == 401
    )


def test_login_unknown_user(client):
    assert (
        client.post(TOKEN_URL, data={"username": "nobody", "password": "secret"}).status_code == 401
    )


def test_login_missing_credentials(client):
    assert client.post(TOKEN_URL, data={}).status_code == 422
