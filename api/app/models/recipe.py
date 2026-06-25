from enum import StrEnum

from pydantic import BaseModel, Field


class DietType(StrEnum):
    VEGAN = "vegan"
    VEGETARIAN = "vegetarian"
    PESCATARIAN = "pescatarian"
    OMNIVORE = "omnivore"


class MealType(StrEnum):
    BREAKFAST = "breakfast"
    LUNCH = "lunch"
    DINNER = "dinner"
    SNACK = "snack"
    DESSERT = "dessert"


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
    prep_time: int | None = None
    cook_time: int | None = None
    diet_type: DietType | None = None
    meal_type: MealType | None = None
    tags: list[str] = []


class IngredientSummary(BaseModel):
    id: int
    name: str

    model_config = {"from_attributes": True}


class RecipeIngredientRead(BaseModel):
    ingredient: IngredientSummary
    quantity: float
    unit: str | None = None

    model_config = {"from_attributes": True}


class TagRead(BaseModel):
    id: int
    name: str

    model_config = {"from_attributes": True}


class RecipeRead(BaseModel):
    id: int
    name: str
    description: str
    prep_time: int | None
    cook_time: int | None
    diet_type: DietType | None
    meal_type: MealType | None
    tags: list[TagRead]
    recipe_ingredients: list[RecipeIngredientRead]
    instructions: list[RecipeStep]

    model_config = {"from_attributes": True}
