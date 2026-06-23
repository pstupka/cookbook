from sqlalchemy.orm import Session

from app.db.schema import Recipe


class RecipeService:
    def __init__(self, session: Session):
        self._db = session

    def list_recipes(self) -> list[Recipe]:
        return self._db.query(Recipe).all()

    def get_recipe(self, recipe_id: int) -> Recipe | None:
        return self._db.query(Recipe).filter(Recipe.id == recipe_id).first()

    def create_recipe(
        self, name: str, description: str, ingredients: list[str], instructions: str
    ) -> Recipe:
        recipe = Recipe(
            name=name,
            description=description,
            ingredients=ingredients,
            instructions=instructions,
        )
        self._db.add(recipe)
        self._db.commit()
        self._db.refresh(recipe)
        return recipe

    def update_recipe(
        self,
        recipe_id: int,
        name: str,
        description: str,
        ingredients: list[str],
        instructions: str,
    ) -> Recipe | None:
        recipe = self.get_recipe(recipe_id)
        if not recipe:
            return None
        recipe.name = name
        recipe.description = description
        recipe.ingredients = ingredients
        recipe.instructions = instructions
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
