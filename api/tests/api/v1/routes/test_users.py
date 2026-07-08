BASE_URL = "/api/v1/users"

PAYLOAD = {
    "username": "johndoe",
    "password": "secret123",
    "email": "john@example.com",
    "full_name": "John Doe",
}


# --- Unauthenticated ---


def test_list_users_requires_auth(client):
    assert client.get(BASE_URL).status_code == 401


def test_create_user_requires_auth(client):
    assert client.post(BASE_URL, json=PAYLOAD).status_code == 401


def test_get_user_requires_auth(client):
    assert client.get(f"{BASE_URL}/1").status_code == 401


def test_update_user_requires_auth(client):
    assert client.put(f"{BASE_URL}/1", json={}).status_code == 401


def test_delete_user_requires_auth(client):
    assert client.delete(f"{BASE_URL}/1").status_code == 401


def test_get_me_requires_auth(client):
    assert client.get(f"{BASE_URL}/me").status_code == 401


# --- Non-admin ---


def test_create_user_requires_admin(regular_client):
    assert regular_client.post(BASE_URL, json=PAYLOAD).status_code == 403


def test_get_me_as_regular_user(regular_client):
    response = regular_client.get(f"{BASE_URL}/me")

    assert response.status_code == 200
    assert response.json()["id"] == 998
    assert response.json()["username"] == "testuser"
    assert response.json()["is_admin"] is False


# --- Admin ---


def test_list_users_empty(admin_client):
    response = admin_client.get(BASE_URL)

    assert response.status_code == 200
    assert response.json() == []


def test_create_user(admin_client):
    response = admin_client.post(BASE_URL, json=PAYLOAD)

    assert response.status_code == 200
    data = response.json()
    assert data["id"] is not None
    assert data["username"] == "johndoe"
    assert data["email"] == "john@example.com"
    assert data["full_name"] == "John Doe"
    assert data["disabled"] is False
    assert data["is_admin"] is False


def test_get_me_as_admin(admin_client):
    response = admin_client.get(f"{BASE_URL}/me")

    assert response.status_code == 200
    assert response.json()["id"] == 999
    assert response.json()["username"] == "testadmin"
    assert response.json()["is_admin"] is True


def test_create_admin_user(admin_client):
    response = admin_client.post(BASE_URL, json={**PAYLOAD, "is_admin": True})

    assert response.status_code == 200
    assert response.json()["is_admin"] is True


def test_create_user_does_not_expose_password(admin_client):
    data = admin_client.post(BASE_URL, json=PAYLOAD).json()

    assert "password" not in data
    assert "hashed_password" not in data


def test_create_user_invalid_email(admin_client):
    assert admin_client.post(BASE_URL, json={**PAYLOAD, "email": "not-an-email"}).status_code == 422


def test_create_user_missing_username(admin_client):
    assert admin_client.post(BASE_URL, json={"password": "secret"}).status_code == 422


def test_list_users_after_create(admin_client):
    admin_client.post(BASE_URL, json=PAYLOAD)
    admin_client.post(
        BASE_URL, json={**PAYLOAD, "username": "janedoe", "email": "jane@example.com"}
    )

    assert len(admin_client.get(BASE_URL).json()) == 2


def test_get_user(admin_client):
    created = admin_client.post(BASE_URL, json=PAYLOAD).json()

    response = admin_client.get(f"{BASE_URL}/{created['id']}")

    assert response.status_code == 200
    assert response.json()["username"] == "johndoe"


def test_get_user_not_found(admin_client):
    assert admin_client.get(f"{BASE_URL}/999").status_code == 404


def test_update_user_username(admin_client):
    created = admin_client.post(BASE_URL, json=PAYLOAD).json()

    response = admin_client.put(f"{BASE_URL}/{created['id']}", json={"username": "janedoe"})

    assert response.status_code == 200
    assert response.json()["username"] == "janedoe"


def test_update_user_email(admin_client):
    created = admin_client.post(BASE_URL, json=PAYLOAD).json()

    response = admin_client.put(f"{BASE_URL}/{created['id']}", json={"email": "new@example.com"})

    assert response.status_code == 200
    assert response.json()["email"] == "new@example.com"


def test_update_user_not_found(admin_client):
    assert admin_client.put(f"{BASE_URL}/999", json={"username": "x"}).status_code == 404


def test_delete_user(admin_client):
    created = admin_client.post(BASE_URL, json=PAYLOAD).json()

    assert admin_client.delete(f"{BASE_URL}/{created['id']}").status_code == 200
    assert admin_client.get(f"{BASE_URL}/{created['id']}").status_code == 404


def test_delete_user_not_found(admin_client):
    assert admin_client.delete(f"{BASE_URL}/999").status_code == 404
