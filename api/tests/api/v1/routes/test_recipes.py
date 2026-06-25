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


def test_create_recipe_empty_name(client):
    response = client.post(BASE_URL, json={**PAYLOAD, "name": ""})

    assert response.status_code == 422


def test_create_recipe_empty_ingredient_name(client):
    payload = {**PAYLOAD, "ingredients": [{"name": "", "quantity": "1", "unit": "cup"}]}

    response = client.post(BASE_URL, json=payload)

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


def test_create_recipe_no_ingredients(client):
    payload = {**PAYLOAD, "ingredients": []}

    response = client.post(BASE_URL, json=payload)

    assert response.status_code == 201
    assert response.json()["recipe_ingredients"] == []


def test_create_recipe_multiple_ingredients(client):
    payload = {
        **PAYLOAD,
        "ingredients": [
            {"name": "Flour", "quantity": "2", "unit": "cups"},
            {"name": "Sugar", "quantity": "1", "unit": "tbsp"},
            {"name": "Salt", "quantity": "0.5", "unit": "tsp"},
        ],
    }

    response = client.post(BASE_URL, json=payload)

    assert response.status_code == 201
    assert len(response.json()["recipe_ingredients"]) == 3


def test_create_recipe_fractional_quantity(client):
    payload = {**PAYLOAD, "ingredients": [{"name": "Yeast", "quantity": "0.5", "unit": "tsp"}]}

    response = client.post(BASE_URL, json=payload)

    assert response.status_code == 201
    assert response.json()["recipe_ingredients"][0]["quantity"] == 0.5


def test_delete_recipe_cascades_to_recipe_ingredients(client, db_session):
    from app.db.schema import RecipeIngredient

    created = client.post(BASE_URL, json=PAYLOAD).json()
    recipe_id = created["id"]

    client.delete(f"{BASE_URL}/{recipe_id}")

    orphans = (
        db_session.query(RecipeIngredient).filter(RecipeIngredient.recipe_id == recipe_id).all()
    )
    assert orphans == []


def test_update_recipe_reuses_existing_ingredient(client, db_session):
    from app.db.schema import Ingredient

    client.post(BASE_URL, json=PAYLOAD)  # creates Flour ingredient
    created = client.post(BASE_URL, json=PAYLOAD).json()  # reuses Flour

    # Update second recipe to also use Flour
    client.put(f"{BASE_URL}/{created['id']}", json=PAYLOAD)

    assert db_session.query(Ingredient).filter(Ingredient.name == "Flour").count() == 1


def test_delete_ingredient_used_in_recipe_orphans_recipe(client):
    # Create a recipe (also creates the Flour ingredient)
    recipe = client.post(BASE_URL, json=PAYLOAD).json()
    ingredient_id = recipe["recipe_ingredients"][0]["ingredient"]["id"]

    # Deleting an ingredient used in a recipe should be rejected
    response = client.delete(f"/api/v1/ingredients/{ingredient_id}")

    assert response.status_code == 409
    # Recipe is unaffected
    assert client.get(f"{BASE_URL}/{recipe['id']}").status_code == 200


# --- metadata tests ---


def test_create_recipe_with_metadata(client):
    payload = {
        **PAYLOAD,
        "prep_time": 15,
        "cook_time": 45,
        "diet_type": "vegan",
        "meal_type": "dinner",
    }

    response = client.post(BASE_URL, json=payload)

    assert response.status_code == 201
    data = response.json()
    assert data["prep_time"] == 15
    assert data["cook_time"] == 45
    assert data["diet_type"] == "vegan"
    assert data["meal_type"] == "dinner"


def test_create_recipe_defaults_metadata_to_none(client):
    response = client.post(BASE_URL, json=PAYLOAD)

    data = response.json()
    assert data["prep_time"] is None
    assert data["cook_time"] is None
    assert data["diet_type"] is None
    assert data["meal_type"] is None
    assert data["tags"] == []


def test_create_recipe_invalid_diet_type(client):
    response = client.post(BASE_URL, json={**PAYLOAD, "diet_type": "carnivore"})

    assert response.status_code == 422


def test_create_recipe_invalid_meal_type(client):
    response = client.post(BASE_URL, json={**PAYLOAD, "meal_type": "brunch"})

    assert response.status_code == 422


def test_create_recipe_with_tags(client):
    payload = {**PAYLOAD, "tags": ["quick", "easy", "gluten-free"]}

    response = client.post(BASE_URL, json=payload)

    assert response.status_code == 201
    tag_names = [t["name"] for t in response.json()["tags"]]
    assert sorted(tag_names) == ["easy", "gluten-free", "quick"]


def test_create_recipe_reuses_existing_tag(client, db_session):
    from app.db.schema import Tag

    client.post(BASE_URL, json={**PAYLOAD, "tags": ["quick"]})
    client.post(BASE_URL, json={**PAYLOAD, "name": "Cake", "tags": ["quick"]})

    assert db_session.query(Tag).filter(Tag.name == "quick").count() == 1


def test_update_recipe_replaces_tags(client):
    created = client.post(BASE_URL, json={**PAYLOAD, "tags": ["quick"]}).json()

    updated = client.put(
        f"{BASE_URL}/{created['id']}", json={**PAYLOAD, "tags": ["slow", "hearty"]}
    ).json()

    tag_names = [t["name"] for t in updated["tags"]]
    assert sorted(tag_names) == ["hearty", "slow"]


def test_update_recipe_clears_tags(client):
    created = client.post(BASE_URL, json={**PAYLOAD, "tags": ["quick"]}).json()

    updated = client.put(f"{BASE_URL}/{created['id']}", json={**PAYLOAD, "tags": []}).json()

    assert updated["tags"] == []


def test_update_recipe_metadata(client):
    created = client.post(BASE_URL, json=PAYLOAD).json()

    updated = client.put(
        f"{BASE_URL}/{created['id']}",
        json={
            **PAYLOAD,
            "prep_time": 10,
            "cook_time": 20,
            "diet_type": "vegetarian",
            "meal_type": "lunch",
        },
    ).json()

    assert updated["prep_time"] == 10
    assert updated["cook_time"] == 20
    assert updated["diet_type"] == "vegetarian"
    assert updated["meal_type"] == "lunch"
