from fastapi import APIRouter, Depends, HTTPException

from app.db.schema import SessionLocal
from app.models.ingredient import IngredientCreate, IngredientRead
from app.services.ingredient_service import IngredientService

router = APIRouter()


def get_ingredient_service() -> IngredientService:
    return IngredientService(session=SessionLocal())


@router.get("/ingredients", response_model=list[IngredientRead])
def list_ingredients(service: IngredientService = Depends(get_ingredient_service)):
    return service.list_ingredients()


@router.post("/ingredients", response_model=IngredientRead, status_code=201)
def create_ingredient(
    ingredient: IngredientCreate,
    service: IngredientService = Depends(get_ingredient_service),
):
    try:
        return service.create_ingredient(ingredient.name, ingredient.default_unit)
    except ValueError as e:
        raise HTTPException(status_code=409, detail=str(e))


@router.delete("/ingredients/{ingredient_id}", status_code=204)
def delete_ingredient(
    ingredient_id: int,
    service: IngredientService = Depends(get_ingredient_service),
):
    success = service.delete_ingredient(ingredient_id)
    if not success:
        raise HTTPException(status_code=404, detail="Ingredient not found")
