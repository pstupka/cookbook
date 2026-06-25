from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.db.schema import Ingredient, RecipeIngredient


class IngredientService:
    def __init__(self, session: Session):
        self._db = session

    def list_ingredients(self) -> list[Ingredient]:
        return self._db.query(Ingredient).order_by(Ingredient.name).all()

    def get_ingredient(self, ingredient_id: int) -> Ingredient | None:
        return self._db.query(Ingredient).filter(Ingredient.id == ingredient_id).first()

    def create_ingredient(self, name: str, default_unit: str | None = None) -> Ingredient:
        ingredient = Ingredient(name=name, default_unit=default_unit)
        self._db.add(ingredient)
        try:
            self._db.commit()
        except IntegrityError:
            self._db.rollback()
            raise ValueError(f"Ingredient '{name}' already exists")
        self._db.refresh(ingredient)
        return ingredient

    def is_in_use(self, ingredient_id: int) -> bool:
        return (
            self._db.query(RecipeIngredient)
            .filter(RecipeIngredient.ingredient_id == ingredient_id)
            .first()
            is not None
        )

    def delete_ingredient(self, ingredient_id: int) -> bool:
        ingredient = self.get_ingredient(ingredient_id)
        if not ingredient:
            return False
        self._db.delete(ingredient)
        self._db.commit()
        return True
