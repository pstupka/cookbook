from enum import StrEnum

from pydantic import BaseModel


class IngredientUnit(StrEnum):
    GRAM = "g"
    KILOGRAM = "kg"
    MILLILITER = "ml"
    LITER = "l"
    CUP = "cup"
    TABLESPOON = "tbsp"
    TEASPOON = "tsp"
    PIECE = "pc"


class IngredientCreate(BaseModel):
    name: str
    default_unit: IngredientUnit | None = None


class IngredientRead(BaseModel):
    id: int
    name: str
    default_unit: IngredientUnit | None = None

    model_config = {"from_attributes": True}
