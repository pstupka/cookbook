from pydantic import BaseModel


class RecipeIngredient(BaseModel):
    name: str
    quantity: str
    unit: str | None = None


class RecipeStep(BaseModel):
    order: int
    text: str
    photo_url: str | None = None


class RecipeCreate(BaseModel):
    name: str
    description: str
    ingredients: list[RecipeIngredient]
    instructions: list[RecipeStep]


class IngredientSummary(BaseModel):
    id: int
    name: str

    model_config = {"from_attributes": True}


class RecipeIngredientRead(BaseModel):
    ingredient: IngredientSummary
    quantity: float
    unit: str | None = None

    model_config = {"from_attributes": True}


class RecipeRead(BaseModel):
    id: int
    name: str
    description: str
    recipe_ingredients: list[RecipeIngredientRead]
    instructions: list[RecipeStep]

    model_config = {"from_attributes": True}
