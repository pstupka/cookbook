from sqlalchemy.orm import Session

from app.db.schema import Ingredient, Recipe, RecipeIngredient


class RecipeService:
    def __init__(self, session: Session):
        self._db = session

    def list_recipes(self) -> list[Recipe]:
        return self._db.query(Recipe).all()

    def get_recipe(self, recipe_id: int) -> Recipe | None:
        return self._db.query(Recipe).filter(Recipe.id == recipe_id).first()

    def _get_or_create_ingredient(self, name: str) -> Ingredient:
        ingredient = self._db.query(Ingredient).filter(Ingredient.name == name).first()
        if not ingredient:
            ingredient = Ingredient(name=name)
            self._db.add(ingredient)
            self._db.flush()
        return ingredient

    def create_recipe(
        self, name: str, description: str, ingredients: list[dict], instructions: list[dict]
    ) -> Recipe:
        recipe = Recipe(
            name=name,
            description=description,
            instructions=instructions,
        )
        self._db.add(recipe)
        self._db.flush()  # Flush to get the recipe ID for the RecipeIngredient entries
        for item in ingredients:
            ingredient = self._get_or_create_ingredient(item["name"])
            recipe_ingredient = RecipeIngredient(
                recipe_id=recipe.id,
                ingredient_id=ingredient.id,
                quantity=float(item["quantity"]),
                unit=item.get("unit"),
            )
            self._db.add(recipe_ingredient)

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
    ) -> Recipe | None:
        recipe = self.get_recipe(recipe_id)
        if not recipe:
            return None
        recipe.name = name
        recipe.description = description
        recipe.instructions = instructions
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

    def delete_recipe(self, recipe_id: int) -> bool:
        recipe = self.get_recipe(recipe_id)
        if not recipe:
            return False
        self._db.delete(recipe)
        self._db.commit()
        return True
