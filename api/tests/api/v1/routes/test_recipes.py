BASE_URL = "/api/v1/recipes"

PAYLOAD = {
    "name": "Bread",
    "description": "Simple bread",
    "ingredients": [{"name": "Flour", "quantity": "2", "unit": "cups"}],
    "instructions": [{"order": 1, "text": "Mix ingredients"}],
}


# --- Auth guards ---


def test_create_recipe_requires_auth(client):
    assert client.post(BASE_URL, json=PAYLOAD).status_code == 401


def test_update_recipe_requires_auth(client):
    assert client.put(f"{BASE_URL}/1", json=PAYLOAD).status_code == 401


def test_delete_recipe_requires_auth(client):
    assert client.delete(f"{BASE_URL}/1").status_code == 401


# --- Read ---


def test_list_recipes_empty(client):
    response = client.get(BASE_URL)

    assert response.status_code == 200
    assert response.json() == []


def test_create_recipe(regular_client):
    response = regular_client.post(BASE_URL, json=PAYLOAD)

    assert response.status_code == 201
    data = response.json()
    assert data["id"] is not None
    assert data["name"] == "Bread"
    assert data["description"] == "Simple bread"
    assert data["visibility"] == "public"
    assert data["owner_id"] == 998
    assert len(data["recipe_ingredients"]) == 1
    assert data["recipe_ingredients"][0]["ingredient"]["name"] == "Flour"
    assert data["recipe_ingredients"][0]["quantity"] == 2.0
    assert data["recipe_ingredients"][0]["unit"] == "cups"


def test_create_recipe_invalid_payload(regular_client):
    response = regular_client.post(BASE_URL, json={"name": "Bread"})

    assert response.status_code == 422


def test_create_recipe_empty_name(regular_client):
    response = regular_client.post(BASE_URL, json={**PAYLOAD, "name": ""})

    assert response.status_code == 422


def test_create_recipe_empty_ingredient_name(regular_client):
    payload = {**PAYLOAD, "ingredients": [{"name": "", "quantity": "1", "unit": "cup"}]}

    response = regular_client.post(BASE_URL, json=payload)

    assert response.status_code == 422


def test_get_recipe(regular_client):
    created = regular_client.post(BASE_URL, json=PAYLOAD).json()

    response = regular_client.get(f"{BASE_URL}/{created['id']}")

    assert response.status_code == 200
    assert response.json()["name"] == "Bread"


def test_get_recipe_not_found(client):
    response = client.get(f"{BASE_URL}/999")

    assert response.status_code == 404


def test_list_recipes_after_create(regular_client):
    regular_client.post(BASE_URL, json=PAYLOAD)
    regular_client.post(BASE_URL, json={**PAYLOAD, "name": "Cake"})

    response = regular_client.get(BASE_URL)

    assert response.status_code == 200
    assert len(response.json()) == 2


def test_update_recipe(regular_client):
    created = regular_client.post(BASE_URL, json=PAYLOAD).json()
    updated_payload = {
        **PAYLOAD,
        "name": "Sourdough",
        "ingredients": [{"name": "Sugar", "quantity": "1", "unit": "tbsp"}],
    }

    response = regular_client.put(f"{BASE_URL}/{created['id']}", json=updated_payload)

    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Sourdough"
    assert data["recipe_ingredients"][0]["ingredient"]["name"] == "Sugar"


def test_update_recipe_not_found(regular_client):
    response = regular_client.put(f"{BASE_URL}/999", json=PAYLOAD)

    assert response.status_code == 404


def test_delete_recipe(regular_client):
    created = regular_client.post(BASE_URL, json=PAYLOAD).json()

    response = regular_client.delete(f"{BASE_URL}/{created['id']}")

    assert response.status_code == 204
    assert regular_client.get(f"{BASE_URL}/{created['id']}").status_code == 404


def test_delete_recipe_not_found(regular_client):
    response = regular_client.delete(f"{BASE_URL}/999")

    assert response.status_code == 404


def test_create_recipe_with_visibility(regular_client):
    payload = {**PAYLOAD, "visibility": "members"}

    response = regular_client.post(BASE_URL, json=payload)

    assert response.status_code == 201
    assert response.json()["visibility"] == "members"


def test_list_recipes_excludes_private_when_no_auth(regular_client):
    regular_client.post(BASE_URL, json={**PAYLOAD, "name": "Public", "visibility": "public"})
    regular_client.post(BASE_URL, json={**PAYLOAD, "name": "Private", "visibility": "private"})

    response = regular_client.get(BASE_URL)

    assert response.status_code == 200
    names = [r["name"] for r in response.json()]
    assert "Public" in names
    assert "Private" not in names


def test_get_private_recipe_returns_403(regular_client):
    created = regular_client.post(BASE_URL, json={**PAYLOAD, "visibility": "private"}).json()

    response = regular_client.get(f"{BASE_URL}/{created['id']}")

    assert response.status_code == 403


def test_create_recipe_no_ingredients(regular_client):
    payload = {**PAYLOAD, "ingredients": []}

    response = regular_client.post(BASE_URL, json=payload)

    assert response.status_code == 201
    assert response.json()["recipe_ingredients"] == []


def test_two_recipes_share_ingredient_with_different_units(regular_client):
    payload_grams = {
        "name": "Chocolate Cake",
        "description": "Rich cake",
        "ingredients": [{"name": "Flour", "quantity": "200", "unit": "g"}],
        "instructions": [{"order": 1, "text": "Mix"}],
    }
    payload_cups = {
        "name": "Pancakes",
        "description": "Fluffy pancakes",
        "ingredients": [{"name": "Flour", "quantity": "1", "unit": "cups"}],
        "instructions": [{"order": 1, "text": "Mix"}],
    }

    cake = regular_client.post(BASE_URL, json=payload_grams).json()
    pancakes = regular_client.post(BASE_URL, json=payload_cups).json()

    assert cake["recipe_ingredients"][0]["ingredient"]["name"] == "Flour"
    assert cake["recipe_ingredients"][0]["unit"] == "g"
    assert pancakes["recipe_ingredients"][0]["ingredient"]["name"] == "Flour"
    assert pancakes["recipe_ingredients"][0]["unit"] == "cups"
    assert (
        cake["recipe_ingredients"][0]["ingredient"]["id"]
        == pancakes["recipe_ingredients"][0]["ingredient"]["id"]
    )


def test_create_recipe_multiple_ingredients(regular_client):
    payload = {
        **PAYLOAD,
        "ingredients": [
            {"name": "Flour", "quantity": "2", "unit": "cups"},
            {"name": "Sugar", "quantity": "1", "unit": "tbsp"},
            {"name": "Salt", "quantity": "0.5", "unit": "tsp"},
        ],
    }

    response = regular_client.post(BASE_URL, json=payload)

    assert response.status_code == 201
    assert len(response.json()["recipe_ingredients"]) == 3


def test_create_recipe_multiple_ingredients_different_units(regular_client):
    payload = {
        **PAYLOAD,
        "ingredients": [
            {"name": "Flour", "quantity": "2", "unit": "cups"},
            {"name": "Flour", "quantity": "2", "unit": "tsp"},
            {"name": "Sugar", "quantity": "1", "unit": "tbsp"},
            {"name": "Salt", "quantity": "0.5", "unit": "tsp"},
        ],
    }

    response = regular_client.post(BASE_URL, json=payload)

    assert response.status_code == 201
    assert len(response.json()["recipe_ingredients"]) == 4


def test_create_recipe_fractional_quantity(regular_client):
    payload = {**PAYLOAD, "ingredients": [{"name": "Yeast", "quantity": "0.5", "unit": "tsp"}]}

    response = regular_client.post(BASE_URL, json=payload)

    assert response.status_code == 201
    assert response.json()["recipe_ingredients"][0]["quantity"] == 0.5


def test_delete_recipe_cascades_to_recipe_ingredients(regular_client, db_session):
    from app.db.schema import RecipeIngredient

    created = regular_client.post(BASE_URL, json=PAYLOAD).json()
    recipe_id = created["id"]

    regular_client.delete(f"{BASE_URL}/{recipe_id}")

    orphans = (
        db_session.query(RecipeIngredient).filter(RecipeIngredient.recipe_id == recipe_id).all()
    )
    assert orphans == []


def test_update_recipe_reuses_existing_ingredient(regular_client, db_session):
    from app.db.schema import Ingredient

    regular_client.post(BASE_URL, json=PAYLOAD)  # creates Flour ingredient
    created = regular_client.post(BASE_URL, json=PAYLOAD).json()  # reuses Flour

    # Update second recipe to also use Flour
    regular_client.put(f"{BASE_URL}/{created['id']}", json=PAYLOAD)

    assert db_session.query(Ingredient).filter(Ingredient.name == "Flour").count() == 1


def test_delete_ingredient_used_in_recipe_orphans_recipe(regular_client):
    # Create a recipe (also creates the Flour ingredient)
    recipe = regular_client.post(BASE_URL, json=PAYLOAD).json()
    ingredient_id = recipe["recipe_ingredients"][0]["ingredient"]["id"]

    # Deleting an ingredient used in a recipe should be rejected
    response = regular_client.delete(f"/api/v1/ingredients/{ingredient_id}")

    assert response.status_code == 409
    # Recipe is unaffected
    assert regular_client.get(f"{BASE_URL}/{recipe['id']}").status_code == 200


# --- metadata tests ---


def test_create_recipe_with_metadata(regular_client):
    payload = {
        **PAYLOAD,
        "prep_time": 15,
        "cook_time": 45,
        "diet_type": "vegan",
        "meal_type": "dinner",
    }

    response = regular_client.post(BASE_URL, json=payload)

    assert response.status_code == 201
    data = response.json()
    assert data["prep_time"] == 15
    assert data["cook_time"] == 45
    assert data["diet_type"] == "vegan"
    assert data["meal_type"] == "dinner"


def test_create_recipe_defaults_metadata_to_none(regular_client):
    response = regular_client.post(BASE_URL, json=PAYLOAD)

    data = response.json()
    assert data["prep_time"] is None
    assert data["cook_time"] is None
    assert data["diet_type"] is None
    assert data["meal_type"] is None
    assert data["tags"] == []


def test_create_recipe_invalid_diet_type(regular_client):
    response = regular_client.post(BASE_URL, json={**PAYLOAD, "diet_type": "carnivore"})

    assert response.status_code == 422


def test_create_recipe_invalid_meal_type(regular_client):
    response = regular_client.post(BASE_URL, json={**PAYLOAD, "meal_type": "brunch"})

    assert response.status_code == 422


def test_create_recipe_with_tags(regular_client):
    payload = {**PAYLOAD, "tags": ["quick", "easy", "gluten-free"]}

    response = regular_client.post(BASE_URL, json=payload)

    assert response.status_code == 201
    tag_names = [t["name"] for t in response.json()["tags"]]
    assert sorted(tag_names) == ["easy", "gluten-free", "quick"]


def test_create_recipe_reuses_existing_tag(regular_client, db_session):
    from app.db.schema import Tag

    regular_client.post(BASE_URL, json={**PAYLOAD, "tags": ["quick"]})
    regular_client.post(BASE_URL, json={**PAYLOAD, "name": "Cake", "tags": ["quick"]})

    assert db_session.query(Tag).filter(Tag.name == "quick").count() == 1


def test_update_recipe_replaces_tags(regular_client):
    created = regular_client.post(BASE_URL, json={**PAYLOAD, "tags": ["quick"]}).json()

    updated = regular_client.put(
        f"{BASE_URL}/{created['id']}", json={**PAYLOAD, "tags": ["slow", "hearty"]}
    ).json()

    tag_names = [t["name"] for t in updated["tags"]]
    assert sorted(tag_names) == ["hearty", "slow"]


def test_update_recipe_clears_tags(regular_client):
    created = regular_client.post(BASE_URL, json={**PAYLOAD, "tags": ["quick"]}).json()

    updated = regular_client.put(f"{BASE_URL}/{created['id']}", json={**PAYLOAD, "tags": []}).json()

    assert updated["tags"] == []


def test_update_recipe_metadata(regular_client):
    created = regular_client.post(BASE_URL, json=PAYLOAD).json()

    updated = regular_client.put(
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
