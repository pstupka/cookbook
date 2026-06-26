from fastapi import APIRouter, Depends, HTTPException

from app.db.schema import SessionLocal
from app.models.recipe import RecipeCreate, RecipeRead
from app.services.recipe_service import RecipeService

router = APIRouter()


def get_recipe_service() -> RecipeService:
    return RecipeService(session=SessionLocal())


@router.get("/recipes", response_model=list[RecipeRead])
def get_recipes(service: RecipeService = Depends(get_recipe_service)):
    return service.list_recipes()


@router.post("/recipes", response_model=RecipeRead, status_code=201)
def create_recipe(recipe: RecipeCreate, service: RecipeService = Depends(get_recipe_service)):
    return service.create_recipe(
        recipe.name,
        recipe.description,
        [i.model_dump() for i in recipe.ingredients],
        [s.model_dump() for s in recipe.instructions],
        prep_time=recipe.prep_time,
        cook_time=recipe.cook_time,
        diet_type=recipe.diet_type,
        meal_type=recipe.meal_type,
        tags=recipe.tags,
        visibility=recipe.visibility,
        owner_id=recipe.owner_id,
    )


@router.get("/recipes/{recipe_id}", response_model=RecipeRead)
def get_recipe(recipe_id: int, service: RecipeService = Depends(get_recipe_service)):
    try:
        return service.get_recipe(recipe_id)
    except LookupError:
        raise HTTPException(status_code=404, detail="Recipe not found")
    except PermissionError:
        raise HTTPException(status_code=403, detail="You do not have access to this recipe")


@router.put("/recipes/{recipe_id}", response_model=RecipeRead)
def update_recipe(
    recipe_id: int,
    recipe: RecipeCreate,
    service: RecipeService = Depends(get_recipe_service),
    current_user_id: int | None = None,
):
    try:
        return service.update_recipe(
            recipe_id,
            recipe.name,
            recipe.description,
            [i.model_dump() for i in recipe.ingredients],
            [s.model_dump() for s in recipe.instructions],
            prep_time=recipe.prep_time,
            cook_time=recipe.cook_time,
            diet_type=recipe.diet_type,
            meal_type=recipe.meal_type,
            tags=recipe.tags,
            visibility=recipe.visibility,
            current_user_id=current_user_id,
        )
    except LookupError:
        raise HTTPException(status_code=404, detail="Recipe not found")
    except PermissionError:
        raise HTTPException(
            status_code=403, detail="You do not have permission to update this recipe"
        )


@router.delete("/recipes/{recipe_id}", status_code=204)
def delete_recipe(recipe_id: int, service: RecipeService = Depends(get_recipe_service)):
    try:
        service.delete_recipe(recipe_id)
    except LookupError:
        raise HTTPException(status_code=404, detail="Recipe not found")
    except PermissionError:
        raise HTTPException(
            status_code=403, detail="You do not have permission to delete this recipe"
        )
