BASE_URL = "/api/v1/users"

PAYLOAD = {
    "username": "johndoe",
    "password": "secret123",
    "email": "john@example.com",
    "full_name": "John Doe",
}


def test_list_users_empty(client):
    response = client.get(BASE_URL)

    assert response.status_code == 200
    assert response.json() == []


def test_create_user(client):
    response = client.post(BASE_URL, json=PAYLOAD)

    assert response.status_code == 200
    data = response.json()
    assert data["id"] is not None
    assert data["username"] == "johndoe"
    assert data["email"] == "john@example.com"
    assert data["full_name"] == "John Doe"
    assert data["disabled"] is False


def test_create_user_does_not_expose_password(client):
    response = client.post(BASE_URL, json=PAYLOAD)

    data = response.json()
    assert "password" not in data
    assert "hashed_password" not in data


def test_create_user_invalid_email(client):
    response = client.post(BASE_URL, json={**PAYLOAD, "email": "not-an-email"})

    assert response.status_code == 422


def test_create_user_missing_username(client):
    response = client.post(BASE_URL, json={"password": "secret"})

    assert response.status_code == 422


def test_list_users_after_create(client):
    client.post(BASE_URL, json=PAYLOAD)
    client.post(BASE_URL, json={**PAYLOAD, "username": "janedoe", "email": "jane@example.com"})

    response = client.get(BASE_URL)

    assert response.status_code == 200
    assert len(response.json()) == 2


def test_get_user(client):
    created = client.post(BASE_URL, json=PAYLOAD).json()

    response = client.get(f"{BASE_URL}/{created['id']}")

    assert response.status_code == 200
    assert response.json()["username"] == "johndoe"


def test_get_user_not_found(client):
    response = client.get(f"{BASE_URL}/999")

    assert response.status_code == 404


def test_update_user_username(client):
    created = client.post(BASE_URL, json=PAYLOAD).json()

    response = client.put(f"{BASE_URL}/{created['id']}", json={"username": "janedoe"})

    assert response.status_code == 200
    assert response.json()["username"] == "janedoe"


def test_update_user_email(client):
    created = client.post(BASE_URL, json=PAYLOAD).json()

    response = client.put(f"{BASE_URL}/{created['id']}", json={"email": "new@example.com"})

    assert response.status_code == 200
    assert response.json()["email"] == "new@example.com"


def test_update_user_not_found(client):
    response = client.put(f"{BASE_URL}/999", json={"username": "x"})

    assert response.status_code == 404


def test_delete_user(client):
    created = client.post(BASE_URL, json=PAYLOAD).json()

    response = client.delete(f"{BASE_URL}/{created['id']}")

    assert response.status_code == 200
    assert client.get(f"{BASE_URL}/{created['id']}").status_code == 404


def test_delete_user_not_found(client):
    response = client.delete(f"{BASE_URL}/999")

    assert response.status_code == 404
