BASE_URL = "/api/v1/ingredients"


# --- Auth guards ---


def test_create_ingredient_requires_auth(client):
    assert client.post(BASE_URL, json={"name": "Salt"}).status_code == 401


def test_patch_ingredient_requires_auth(client):
    assert client.patch(f"{BASE_URL}/1", json={"name": "Salt"}).status_code == 401


def test_delete_ingredient_requires_auth(client):
    assert client.delete(f"{BASE_URL}/1").status_code == 401


# --- Read ---


def test_list_ingredients_empty(client):
    response = client.get(BASE_URL)

    assert response.status_code == 200
    assert response.json() == []


# --- Authenticated write ---


def test_create_ingredient(regular_client):
    response = regular_client.post(BASE_URL, json={"name": "Salt", "default_unit": "tsp"})

    assert response.status_code == 201
    data = response.json()
    assert data["id"] is not None
    assert data["name"] == "Salt"
    assert data["default_unit"] == "tsp"


def test_create_ingredient_no_unit(regular_client):
    response = regular_client.post(BASE_URL, json={"name": "Garlic"})

    assert response.status_code == 201
    assert response.json()["default_unit"] is None


def test_create_ingredient_unknown_unit(regular_client):
    response = regular_client.post(BASE_URL, json={"name": "Pepper", "default_unit": "unknown"})

    assert response.status_code == 422


def test_create_ingredient_duplicate_returns_409(regular_client):
    regular_client.post(BASE_URL, json={"name": "Salt"})

    response = regular_client.post(BASE_URL, json={"name": "Salt"})

    assert response.status_code == 409


def test_create_ingredient_invalid_payload(regular_client):
    response = regular_client.post(BASE_URL, json={})

    assert response.status_code == 422


def test_create_ingredient_empty_name(regular_client):
    response = regular_client.post(BASE_URL, json={"name": ""})

    assert response.status_code == 422


def test_list_ingredients_after_create(regular_client):
    regular_client.post(BASE_URL, json={"name": "Pepper"})
    regular_client.post(BASE_URL, json={"name": "Salt"})

    response = regular_client.get(BASE_URL)

    assert response.status_code == 200
    assert len(response.json()) == 2


def test_delete_ingredient(regular_client):
    created = regular_client.post(BASE_URL, json={"name": "Butter"}).json()

    response = regular_client.delete(f"{BASE_URL}/{created['id']}")

    assert response.status_code == 204


def test_delete_ingredient_not_found(regular_client):
    response = regular_client.delete(f"{BASE_URL}/999")

    assert response.status_code == 404


def test_delete_ingredient_referenced_by_recipe_returns_409(regular_client):
    recipe_payload = {
        "name": "Bread",
        "description": "desc",
        "ingredients": [{"name": "Flour", "quantity": "2", "unit": "cups"}],
        "instructions": [{"order": 1, "text": "Mix"}],
    }
    regular_client.post("/api/v1/recipes", json=recipe_payload)
    ingredient = regular_client.get(BASE_URL).json()[0]

    response = regular_client.delete(f"{BASE_URL}/{ingredient['id']}")

    assert response.status_code == 409


def test_patch_ingredient(regular_client):
    created = regular_client.post(BASE_URL, json={"name": "Salt", "default_unit": "tsp"}).json()

    response = regular_client.patch(
        f"{BASE_URL}/{created['id']}", json={"name": "Sea Salt", "default_unit": "g"}
    )

    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Sea Salt"
    assert data["default_unit"] == "g"


def test_patch_ingredient_not_found(regular_client):
    response = regular_client.patch(f"{BASE_URL}/999", json={"name": "Ghost"})

    assert response.status_code == 404


def test_patch_ingredient_duplicate_name_returns_409(regular_client):
    regular_client.post(BASE_URL, json={"name": "Salt"})
    other = regular_client.post(BASE_URL, json={"name": "Pepper"}).json()

    response = regular_client.patch(f"{BASE_URL}/{other['id']}", json={"name": "Salt"})

    assert response.status_code == 409


def test_patch_ingredient_invalid_payload_returns_422(regular_client):
    created = regular_client.post(BASE_URL, json={"name": "Salt"}).json()

    response = regular_client.patch(f"{BASE_URL}/{created['id']}", json={"name": ""})

    assert response.status_code == 422
