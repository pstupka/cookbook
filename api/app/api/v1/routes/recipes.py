from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api.v1.deps import get_current_user, get_db, get_optional_current_user
from app.db.schema import User as UserORM
from app.models.recipe import RecipeCreate, RecipeRead
from app.services.recipe_service import RecipeService

router = APIRouter()


def get_recipe_service(db: Session = Depends(get_db)) -> RecipeService:
    return RecipeService(session=db)


@router.get("/recipes", response_model=list[RecipeRead])
def get_recipes(
    service: RecipeService = Depends(get_recipe_service),
    current_user: UserORM | None = Depends(get_optional_current_user),
):
    return service.list_recipes(current_user_id=current_user.id if current_user else None)


@router.post("/recipes", response_model=RecipeRead, status_code=201)
def create_recipe(
    recipe: RecipeCreate,
    service: RecipeService = Depends(get_recipe_service),
    current_user: UserORM = Depends(get_current_user),
):
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
        owner_id=current_user.id,
    )


@router.get("/recipes/{recipe_id}", response_model=RecipeRead)
def get_recipe(
    recipe_id: int,
    service: RecipeService = Depends(get_recipe_service),
    current_user: UserORM | None = Depends(get_optional_current_user),
):
    try:
        return service.get_recipe(
            recipe_id, current_user_id=current_user.id if current_user else None
        )
    except LookupError:
        raise HTTPException(status_code=404, detail="Recipe not found")
    except PermissionError:
        raise HTTPException(status_code=403, detail="You do not have access to this recipe")


@router.put("/recipes/{recipe_id}", response_model=RecipeRead)
def update_recipe(
    recipe_id: int,
    recipe: RecipeCreate,
    service: RecipeService = Depends(get_recipe_service),
    current_user: UserORM = Depends(get_current_user),
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
            current_user_id=current_user.id,
        )
    except LookupError:
        raise HTTPException(status_code=404, detail="Recipe not found")
    except PermissionError:
        raise HTTPException(
            status_code=403, detail="You do not have permission to update this recipe"
        )


@router.delete("/recipes/{recipe_id}", status_code=204)
def delete_recipe(
    recipe_id: int,
    service: RecipeService = Depends(
        get_recipe_service,
    ),
    current_user: UserORM = Depends(get_current_user),
):
    try:
        service.delete_recipe(recipe_id, current_user.id)
    except LookupError:
        raise HTTPException(status_code=404, detail="Recipe not found")
    except PermissionError:
        raise HTTPException(
            status_code=403, detail="You do not have permission to delete this recipe"
        )
