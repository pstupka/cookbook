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
