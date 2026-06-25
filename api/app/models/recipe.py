from pydantic import BaseModel, Field


class RecipeIngredient(BaseModel):
    name: str = Field(min_length=1)
    quantity: str
    unit: str | None = None


class RecipeStep(BaseModel):
    order: int
    text: str = Field(min_length=1)
    photo_url: str | None = None


class RecipeCreate(BaseModel):
    name: str = Field(min_length=1)
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
