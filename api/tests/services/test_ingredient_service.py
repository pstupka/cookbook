import pytest

from app.services.ingredient_service import IngredientService


@pytest.fixture()
def service(db_session):
    return IngredientService(session=db_session)


def test_list_ingredients_empty(service):
    assert service.list_ingredients() == []


def test_create_ingredient(service):
    ingredient = service.create_ingredient("Salt", default_unit="tsp")

    assert ingredient.id is not None
    assert ingredient.name == "Salt"
    assert ingredient.default_unit == "tsp"


def test_create_ingredient_no_unit(service):
    ingredient = service.create_ingredient("Garlic")

    assert ingredient.name == "Garlic"
    assert ingredient.default_unit is None


def test_create_ingredient_duplicate_raises(service):
    service.create_ingredient("Salt")

    with pytest.raises(ValueError, match="Salt"):
        service.create_ingredient("Salt")


def test_list_ingredients_returns_all(service):
    service.create_ingredient("Pepper")
    service.create_ingredient("Salt")

    ingredients = service.list_ingredients()

    assert len(ingredients) == 2
    assert [i.name for i in ingredients] == ["Pepper", "Salt"]  # ordered by name


def test_get_ingredient_found(service):
    created = service.create_ingredient("Olive Oil")

    result = service.get_ingredient(created.id)

    assert result is not None
    assert result.name == "Olive Oil"


def test_get_ingredient_not_found(service):
    result = service.get_ingredient(999)

    assert result is None


def test_delete_ingredient(service):
    ingredient = service.create_ingredient("Butter")

    deleted = service.delete_ingredient(ingredient.id)

    assert deleted is True
    assert service.get_ingredient(ingredient.id) is None


def test_delete_ingredient_not_found(service):
    result = service.delete_ingredient(999)

    assert result is False


def test_update_ingredient_name(service):
    ingredient = service.create_ingredient("Salt", default_unit="tsp")

    updated = service.update_ingredient(ingredient.id, name="Sea Salt")

    assert updated is not None
    assert updated.name == "Sea Salt"
    assert updated.default_unit == "tsp"


def test_update_ingredient_default_unit(service):
    ingredient = service.create_ingredient("Flour")

    updated = service.update_ingredient(ingredient.id, default_unit="g")

    assert updated is not None
    assert updated.name == "Flour"
    assert updated.default_unit == "g"


def test_update_ingredient_both_fields(service):
    ingredient = service.create_ingredient("Sugar", default_unit="g")

    updated = service.update_ingredient(ingredient.id, name="Brown Sugar", default_unit="tbsp")

    assert updated is not None
    assert updated.name == "Brown Sugar"
    assert updated.default_unit == "tbsp"


def test_update_ingredient_not_found_returns_none(service):
    result = service.update_ingredient(999, name="Ghost")

    assert result is None


def test_update_ingredient_duplicate_name_raises(service):
    service.create_ingredient("Salt")
    other = service.create_ingredient("Pepper")

    with pytest.raises(ValueError, match="Salt"):
        service.update_ingredient(other.id, name="Salt")


def test_update_ingredient_none_args_leaves_fields_unchanged(service):
    ingredient = service.create_ingredient("Olive Oil", default_unit="ml")

    updated = service.update_ingredient(ingredient.id)

    assert updated is not None
    assert updated.name == "Olive Oil"
    assert updated.default_unit == "ml"
