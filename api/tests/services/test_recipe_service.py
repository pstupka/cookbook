import pytest

from app.services.recipe_service import RecipeService

INGREDIENTS = [{"name": "Flour", "quantity": "2", "unit": "cups"}]
INSTRUCTIONS = [{"order": 1, "text": "Mix ingredients"}]


@pytest.fixture()
def service(db_session):
    return RecipeService(session=db_session)


def test_list_recipes_empty(service):
    assert service.list_recipes() == []


def test_create_recipe(service):
    recipe = service.create_recipe("Bread", "Simple bread", INGREDIENTS, INSTRUCTIONS)

    assert recipe.id is not None
    assert recipe.name == "Bread"
    assert recipe.description == "Simple bread"
    assert recipe.instructions == INSTRUCTIONS


def test_create_recipe_creates_ingredient(service):
    recipe = service.create_recipe("Bread", "Simple bread", INGREDIENTS, INSTRUCTIONS)

    assert len(recipe.recipe_ingredients) == 1
    assert recipe.recipe_ingredients[0].ingredient.name == "Flour"
    assert recipe.recipe_ingredients[0].quantity == 2.0
    assert recipe.recipe_ingredients[0].unit == "cups"


def test_create_recipe_reuses_existing_ingredient(service, db_session):
    service.create_recipe("Bread", "Simple bread", INGREDIENTS, INSTRUCTIONS)
    service.create_recipe("Cake", "Simple cake", INGREDIENTS, INSTRUCTIONS)

    from app.db.schema import Ingredient

    ingredients = db_session.query(Ingredient).all()
    assert len(ingredients) == 1  # Flour created only once


def test_create_recipe_ingredient_without_unit(service):
    ingredients = [{"name": "Sugar", "quantity": "1"}]
    recipe = service.create_recipe("Sweet thing", "desc", ingredients, INSTRUCTIONS)

    assert recipe.recipe_ingredients[0].unit is None


def test_get_recipe_found(service):
    created = service.create_recipe("Pasta", "Italian pasta", INGREDIENTS, INSTRUCTIONS)

    result = service.get_recipe(created.id)

    assert result is not None
    assert result.name == "Pasta"


def test_get_recipe_not_found(service):
    with pytest.raises(LookupError):
        service.get_recipe(999)


def test_list_recipes_returns_all(service):
    service.create_recipe("Bread", "desc", INGREDIENTS, INSTRUCTIONS)
    service.create_recipe("Cake", "desc", INGREDIENTS, INSTRUCTIONS)

    recipes = service.list_recipes()

    assert len(recipes) == 2


def test_update_recipe(service):
    recipe = service.create_recipe("Bread", "old desc", INGREDIENTS, INSTRUCTIONS)
    new_ingredients = [{"name": "Sugar", "quantity": "3", "unit": "tbsp"}]

    updated = service.update_recipe(
        recipe.id, "Sweet Bread", "new desc", new_ingredients, INSTRUCTIONS
    )

    assert updated is not None
    assert updated.name == "Sweet Bread"
    assert updated.description == "new desc"
    assert len(updated.recipe_ingredients) == 1
    assert updated.recipe_ingredients[0].ingredient.name == "Sugar"


def test_update_recipe_replaces_ingredients(service):
    recipe = service.create_recipe("Bread", "desc", INGREDIENTS, INSTRUCTIONS)
    new_ingredients = [
        {"name": "Sugar", "quantity": "1", "unit": "cup"},
        {"name": "Butter", "quantity": "2", "unit": "tbsp"},
    ]

    updated = service.update_recipe(recipe.id, "Cake", "desc", new_ingredients, INSTRUCTIONS)

    assert len(updated.recipe_ingredients) == 2


def test_update_recipe_not_found(service):
    with pytest.raises(LookupError):
        service.update_recipe(999, "Name", "desc", INGREDIENTS, INSTRUCTIONS)


def test_delete_recipe(service):
    recipe = service.create_recipe("Bread", "desc", INGREDIENTS, INSTRUCTIONS)

    service.delete_recipe(recipe.id)

    with pytest.raises(LookupError):
        service.get_recipe(recipe.id)


def test_delete_recipe_not_found(service):
    with pytest.raises(LookupError):
        service.delete_recipe(999)


def test_create_recipe_defaults_to_public(service):
    recipe = service.create_recipe("Bread", "desc", INGREDIENTS, INSTRUCTIONS)

    assert recipe.visibility == "public"
    assert recipe.owner_id is None


def test_create_recipe_with_visibility_and_owner(service):
    recipe = service.create_recipe(
        "Bread", "desc", INGREDIENTS, INSTRUCTIONS, visibility="private", owner_id=1
    )

    assert recipe.visibility == "private"
    assert recipe.owner_id == 1


def test_get_private_recipe_wrong_user_raises(service):
    recipe = service.create_recipe(
        "Secret", "desc", INGREDIENTS, INSTRUCTIONS, visibility="private", owner_id=1
    )

    with pytest.raises(PermissionError):
        service.get_recipe(recipe.id, current_user_id=2)


def test_get_private_recipe_by_owner_succeeds(service):
    recipe = service.create_recipe(
        "Secret", "desc", INGREDIENTS, INSTRUCTIONS, visibility="private", owner_id=1
    )

    result = service.get_recipe(recipe.id, current_user_id=1)

    assert result.id == recipe.id


def test_get_members_recipe_unauthenticated_raises(service):
    recipe = service.create_recipe(
        "Members Only", "desc", INGREDIENTS, INSTRUCTIONS, visibility="members"
    )

    with pytest.raises(PermissionError):
        service.get_recipe(recipe.id, current_user_id=None)


def test_list_recipes_unauthenticated_excludes_private_and_members(service):
    service.create_recipe("Public", "desc", INGREDIENTS, INSTRUCTIONS, visibility="public")
    service.create_recipe("Members", "desc", INGREDIENTS, INSTRUCTIONS, visibility="members")
    service.create_recipe("Private", "desc", INGREDIENTS, INSTRUCTIONS, visibility="private")

    recipes = service.list_recipes(current_user_id=None)

    assert len(recipes) == 1
    assert recipes[0].name == "Public"


def test_list_recipes_authenticated_excludes_others_private(service):
    service.create_recipe("Public", "desc", INGREDIENTS, INSTRUCTIONS, visibility="public")
    service.create_recipe("Members", "desc", INGREDIENTS, INSTRUCTIONS, visibility="members")
    service.create_recipe(
        "Other Private", "desc", INGREDIENTS, INSTRUCTIONS, visibility="private", owner_id=99
    )
    service.create_recipe(
        "Own Private", "desc", INGREDIENTS, INSTRUCTIONS, visibility="private", owner_id=1
    )

    recipes = service.list_recipes(current_user_id=1)

    names = {r.name for r in recipes}
    assert names == {"Public", "Members", "Own Private"}


def test_update_recipe_non_owner_raises(service):
    recipe = service.create_recipe(
        "Bread", "desc", INGREDIENTS, INSTRUCTIONS, visibility="members", owner_id=1
    )

    with pytest.raises(PermissionError):
        service.update_recipe(
            recipe.id, "Hacked", "desc", INGREDIENTS, INSTRUCTIONS, current_user_id=2
        )


def test_delete_recipe_non_owner_raises(service):
    recipe = service.create_recipe("Bread", "desc", INGREDIENTS, INSTRUCTIONS, owner_id=1)

    with pytest.raises(PermissionError):
        service.delete_recipe(recipe.id, current_user_id=2)
