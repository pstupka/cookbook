BASE_URL = "/api/v1/ingredients"


def test_list_ingredients_empty(client):
    response = client.get(BASE_URL)

    assert response.status_code == 200
    assert response.json() == []


def test_create_ingredient(client):
    response = client.post(BASE_URL, json={"name": "Salt", "default_unit": "tsp"})

    assert response.status_code == 201
    data = response.json()
    assert data["id"] is not None
    assert data["name"] == "Salt"
    assert data["default_unit"] == "tsp"


def test_create_ingredient_no_unit(client):
    response = client.post(BASE_URL, json={"name": "Garlic"})

    assert response.status_code == 201
    assert response.json()["default_unit"] is None


def test_create_ingredient_unknown_unit(client):
    response = client.post(BASE_URL, json={"name": "Pepper", "default_unit": "unknown"})

    assert response.status_code == 422


def test_create_ingredient_duplicate_returns_409(client):
    client.post(BASE_URL, json={"name": "Salt"})

    response = client.post(BASE_URL, json={"name": "Salt"})

    assert response.status_code == 409


def test_create_ingredient_invalid_payload(client):
    response = client.post(BASE_URL, json={})

    assert response.status_code == 422


def test_create_ingredient_empty_name(client):
    response = client.post(BASE_URL, json={"name": ""})

    assert response.status_code == 422


def test_list_ingredients_after_create(client):
    client.post(BASE_URL, json={"name": "Pepper"})
    client.post(BASE_URL, json={"name": "Salt"})

    response = client.get(BASE_URL)

    assert response.status_code == 200
    assert len(response.json()) == 2


def test_delete_ingredient(client):
    created = client.post(BASE_URL, json={"name": "Butter"}).json()

    response = client.delete(f"{BASE_URL}/{created['id']}")

    assert response.status_code == 204


def test_delete_ingredient_not_found(client):
    response = client.delete(f"{BASE_URL}/999")

    assert response.status_code == 404


def test_delete_ingredient_referenced_by_recipe_succeeds(client):
    # Deleting an ingredient used in a recipe is now rejected with 409
    recipe_payload = {
        "name": "Bread",
        "description": "desc",
        "ingredients": [{"name": "Flour", "quantity": "2", "unit": "cups"}],
        "instructions": [{"order": 1, "text": "Mix"}],
    }
    client.post("/api/v1/recipes", json=recipe_payload)
    ingredient = client.get(BASE_URL).json()[0]

    response = client.delete(f"{BASE_URL}/{ingredient['id']}")

    assert response.status_code == 409


def test_patch_ingredient(client):
    created = client.post(BASE_URL, json={"name": "Salt", "default_unit": "tsp"}).json()

    response = client.patch(
        f"{BASE_URL}/{created['id']}", json={"name": "Sea Salt", "default_unit": "g"}
    )

    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Sea Salt"
    assert data["default_unit"] == "g"


def test_patch_ingredient_not_found(client):
    response = client.patch(f"{BASE_URL}/999", json={"name": "Ghost"})

    assert response.status_code == 404


def test_patch_ingredient_duplicate_name_returns_409(client):
    client.post(BASE_URL, json={"name": "Salt"})
    other = client.post(BASE_URL, json={"name": "Pepper"}).json()

    response = client.patch(f"{BASE_URL}/{other['id']}", json={"name": "Salt"})

    assert response.status_code == 409


def test_patch_ingredient_invalid_payload_returns_422(client):
    created = client.post(BASE_URL, json={"name": "Salt"}).json()

    response = client.patch(f"{BASE_URL}/{created['id']}", json={"name": ""})

    assert response.status_code == 422
