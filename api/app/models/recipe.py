from pydantic import BaseModel


class Ingredient(BaseModel):
    name: str
    quantity: str
    unit: str | None = None


class RecipeCreate(BaseModel):
    name: str
    description: str
    ingredients: list[Ingredient]
    instructions: str


class RecipeRead(BaseModel):
    id: int
    name: str
    description: str
    ingredients: list[Ingredient]
    instructions: str

    model_config = {"from_attributes": True}
