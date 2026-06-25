BASE_URL = "/api/v1/recipes"

PAYLOAD = {
    "name": "Bread",
    "description": "Simple bread",
    "ingredients": [{"name": "Flour", "quantity": "2", "unit": "cups"}],
    "instructions": [{"order": 1, "text": "Mix ingredients"}],
}


def test_list_recipes_empty(client):
    response = client.get(BASE_URL)

    assert response.status_code == 200
    assert response.json() == []


def test_create_recipe(client):
    response = client.post(BASE_URL, json=PAYLOAD)

    assert response.status_code == 201
    data = response.json()
    assert data["id"] is not None
    assert data["name"] == "Bread"
    assert data["description"] == "Simple bread"
    assert len(data["recipe_ingredients"]) == 1
    assert data["recipe_ingredients"][0]["ingredient"]["name"] == "Flour"
    assert data["recipe_ingredients"][0]["quantity"] == 2.0
    assert data["recipe_ingredients"][0]["unit"] == "cups"


def test_create_recipe_invalid_payload(client):
    response = client.post(BASE_URL, json={"name": "Bread"})

    assert response.status_code == 422


def test_get_recipe(client):
    created = client.post(BASE_URL, json=PAYLOAD).json()

    response = client.get(f"{BASE_URL}/{created['id']}")

    assert response.status_code == 200
    assert response.json()["name"] == "Bread"


def test_get_recipe_not_found(client):
    response = client.get(f"{BASE_URL}/999")

    assert response.status_code == 404


def test_list_recipes_after_create(client):
    client.post(BASE_URL, json=PAYLOAD)
    client.post(BASE_URL, json={**PAYLOAD, "name": "Cake"})

    response = client.get(BASE_URL)

    assert response.status_code == 200
    assert len(response.json()) == 2


def test_update_recipe(client):
    created = client.post(BASE_URL, json=PAYLOAD).json()
    updated_payload = {
        **PAYLOAD,
        "name": "Sourdough",
        "ingredients": [{"name": "Sugar", "quantity": "1", "unit": "tbsp"}],
    }

    response = client.put(f"{BASE_URL}/{created['id']}", json=updated_payload)

    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Sourdough"
    assert data["recipe_ingredients"][0]["ingredient"]["name"] == "Sugar"


def test_update_recipe_not_found(client):
    response = client.put(f"{BASE_URL}/999", json=PAYLOAD)

    assert response.status_code == 404


def test_delete_recipe(client):
    created = client.post(BASE_URL, json=PAYLOAD).json()

    response = client.delete(f"{BASE_URL}/{created['id']}")

    assert response.status_code == 204
    assert client.get(f"{BASE_URL}/{created['id']}").status_code == 404


def test_delete_recipe_not_found(client):
    response = client.delete(f"{BASE_URL}/999")

    assert response.status_code == 404
