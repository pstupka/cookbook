from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api.v1.deps import get_current_user, get_db
from app.db.schema import User as UserORM
from app.models.ingredient import IngredientCreate, IngredientRead
from app.services.ingredient_service import IngredientService

router = APIRouter()


def get_ingredient_service(db: Session = Depends(get_db)) -> IngredientService:
    return IngredientService(session=db)


@router.get("/ingredients", response_model=list[IngredientRead])
def list_ingredients(service: IngredientService = Depends(get_ingredient_service)):
    return service.list_ingredients()


@router.post("/ingredients", response_model=IngredientRead, status_code=201)
def create_ingredient(
    ingredient: IngredientCreate,
    service: IngredientService = Depends(get_ingredient_service),
    _: UserORM = Depends(get_current_user),
):
    try:
        return service.create_ingredient(ingredient.name, ingredient.default_unit)
    except ValueError as e:
        raise HTTPException(status_code=409, detail=str(e))


@router.patch("/ingredients/{ingredient_id}", response_model=IngredientRead)
def patch_ingredient(
    ingredient_id: int,
    ingredient: IngredientCreate,
    service: IngredientService = Depends(get_ingredient_service),
    _: UserORM = Depends(get_current_user),
):
    try:
        updated_ingredient = service.update_ingredient(
            ingredient_id, ingredient.name, ingredient.default_unit
        )
        if not updated_ingredient:
            raise HTTPException(status_code=404, detail="Ingredient not found")
        return updated_ingredient
    except ValueError as e:
        raise HTTPException(status_code=409, detail=str(e))


@router.delete("/ingredients/{ingredient_id}", status_code=204)
def delete_ingredient(
    ingredient_id: int,
    service: IngredientService = Depends(get_ingredient_service),
    _: UserORM = Depends(get_current_user),
):
    if service.is_in_use(ingredient_id):
        raise HTTPException(status_code=409, detail="Ingredient is used in one or more recipes")
    success = service.delete_ingredient(ingredient_id)
    if not success:
        raise HTTPException(status_code=404, detail="Ingredient not found")
