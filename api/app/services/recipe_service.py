from sqlalchemy import or_
from sqlalchemy.orm import Session

from app.db.schema import Ingredient, Recipe, RecipeIngredient, Tag


class RecipeService:
    def __init__(self, session: Session):
        self._db = session

    def list_recipes(self, current_user_id: int | None = None) -> list[Recipe]:
        query = self._db.query(Recipe)
        if current_user_id is None:
            query = query.filter(Recipe.visibility == "public")
        else:
            query = query.filter(
                or_(
                    Recipe.visibility == "public",
                    Recipe.visibility == "members",
                    Recipe.owner_id == current_user_id,
                )
            )
        return query.all()

    def get_recipe(self, recipe_id: int, current_user_id: int | None = None) -> Recipe:
        recipe = self._db.query(Recipe).filter(Recipe.id == recipe_id).first()
        if not recipe:
            raise LookupError(f"Recipe {recipe_id} not found")
        if recipe.visibility == "private" and recipe.owner_id != current_user_id:
            raise PermissionError("You do not own this recipe")
        if recipe.visibility == "members" and current_user_id is None:
            raise PermissionError("You do not have access to this recipe")
        return recipe

    def _get_or_create_ingredient(self, name: str) -> Ingredient:
        ingredient = self._db.query(Ingredient).filter(Ingredient.name == name).first()
        if not ingredient:
            ingredient = Ingredient(name=name)
            self._db.add(ingredient)
            self._db.flush()
        return ingredient

    def _get_or_create_tag(self, name: str) -> Tag:
        tag = self._db.query(Tag).filter(Tag.name == name).first()
        if not tag:
            tag = Tag(name=name)
            self._db.add(tag)
            self._db.flush()
        return tag

    def create_recipe(
        self,
        name: str,
        description: str,
        ingredients: list[dict],
        instructions: list[dict],
        prep_time: int | None = None,
        cook_time: int | None = None,
        diet_type: str | None = None,
        meal_type: str | None = None,
        tags: list[str] | None = None,
        visibility: str = "public",
        owner_id: int | None = None,
    ) -> Recipe:
        recipe = Recipe(
            name=name,
            description=description,
            instructions=instructions,
            prep_time=prep_time,
            cook_time=cook_time,
            diet_type=diet_type,
            meal_type=meal_type,
            visibility=visibility,
            owner_id=owner_id,
        )
        self._db.add(recipe)
        self._db.flush()
        for item in ingredients:
            ingredient = self._get_or_create_ingredient(item["name"])
            self._db.add(
                RecipeIngredient(
                    recipe_id=recipe.id,
                    ingredient_id=ingredient.id,
                    quantity=float(item["quantity"]),
                    unit=item.get("unit"),
                )
            )
        recipe.tags = [self._get_or_create_tag(t) for t in (tags or [])]
        self._db.commit()
        self._db.refresh(recipe)
        return recipe

    def update_recipe(
        self,
        recipe_id: int,
        name: str,
        description: str,
        ingredients: list[dict],
        instructions: list[dict],
        prep_time: int | None = None,
        cook_time: int | None = None,
        diet_type: str | None = None,
        meal_type: str | None = None,
        tags: list[str] | None = None,
        visibility: str | None = None,
        current_user_id: int | None = None,
    ) -> Recipe:
        recipe = self.get_recipe(recipe_id, current_user_id=current_user_id)
        if recipe.owner_id is not None and recipe.owner_id != current_user_id:
            raise PermissionError("You do not own this recipe")
        if visibility is not None:
            recipe.visibility = visibility
        recipe.name = name
        recipe.description = description
        recipe.instructions = instructions
        recipe.prep_time = prep_time
        recipe.cook_time = cook_time
        recipe.diet_type = diet_type
        recipe.meal_type = meal_type
        recipe.tags = [self._get_or_create_tag(t) for t in (tags or [])]
        self._db.query(RecipeIngredient).filter(RecipeIngredient.recipe_id == recipe_id).delete()
        for item in ingredients:
            ing = self._get_or_create_ingredient(item["name"])
            self._db.add(
                RecipeIngredient(
                    recipe_id=recipe.id,
                    ingredient_id=ing.id,
                    quantity=float(item["quantity"]),
                    unit=item.get("unit"),
                )
            )
        self._db.commit()
        self._db.refresh(recipe)
        return recipe

    def delete_recipe(self, recipe_id: int, current_user_id: int | None = None) -> None:
        recipe = self.get_recipe(recipe_id, current_user_id=current_user_id)
        if recipe.owner_id is not None and recipe.owner_id != current_user_id:
            raise PermissionError("You do not own this recipe")
        self._db.delete(recipe)
        self._db.commit()
