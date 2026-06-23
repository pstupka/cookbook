from fastapi import APIRouter, Depends, HTTPException

from app.db.schema import SessionLocal
from app.models.recipe import RecipeCreate, RecipeRead
from app.services.recipe_serrvice import RecipeService

router = APIRouter()


def get_recipe_service() -> RecipeService:
    return RecipeService(session=SessionLocal())


@router.get("/recipes", response_model=list[RecipeRead])
def get_recipes(service: RecipeService = Depends(get_recipe_service)):
    return service.list_recipes()


@router.post("/recipes", response_model=RecipeRead, status_code=201)
def create_recipe(recipe: RecipeCreate, service: RecipeService = Depends(get_recipe_service)):
    return service.create_recipe(
        recipe.name, recipe.description, recipe.ingredients, recipe.instructions
    )


@router.get("/recipes/{recipe_id}", response_model=RecipeRead)
def get_recipe(recipe_id: int, service: RecipeService = Depends(get_recipe_service)):
    recipe = service.get_recipe(recipe_id)
    if not recipe:
        raise HTTPException(status_code=404, detail="Recipe not found")
    return recipe


@router.put("/recipes/{recipe_id}", response_model=RecipeRead)
def update_recipe(
    recipe_id: int,
    recipe: RecipeCreate,
    service: RecipeService = Depends(get_recipe_service),
):
    updated = service.update_recipe(
        recipe_id, recipe.name, recipe.description, recipe.ingredients, recipe.instructions
    )
    if not updated:
        raise HTTPException(status_code=404, detail="Recipe not found")
    return updated


@router.delete("/recipes/{recipe_id}", status_code=204)
def delete_recipe(recipe_id: int, service: RecipeService = Depends(get_recipe_service)):
    success = service.delete_recipe(recipe_id)
    if not success:
        raise HTTPException(status_code=404, detail="Recipe not found")
