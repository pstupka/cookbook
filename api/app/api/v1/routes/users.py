from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api.v1.deps import get_current_user, get_db
from app.db.schema import User as UserORM
from app.models.user import UserCreate, UserRead, UserUpdate
from app.services.user_service import UserService

router = APIRouter()


def get_user_service(db: Session = Depends(get_db)) -> UserService:
    return UserService(session=db)


@router.get("/users", response_model=list[UserRead])
def get_users(
    service: UserService = Depends(get_user_service),
    _: UserORM = Depends(get_current_user),
):
    return service.list_users()


@router.post("/users", response_model=UserRead)
def create_user(
    user: UserCreate,
    service: UserService = Depends(get_user_service),
    current_user: UserORM = Depends(get_current_user),
):
    if not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Admin access required")

    return service.create_user(
        username=user.username,
        password=user.password,
        email=user.email,
        full_name=user.full_name,
        is_admin=user.is_admin,
    )


@router.get("/users/me", response_model=UserRead)
def read_users_me(current_user: UserORM = Depends(get_current_user)) -> UserRead:
    return current_user


@router.get("/users/{user_id}", response_model=UserRead)
def get_user(
    user_id: int,
    service: UserService = Depends(get_user_service),
    _: UserORM = Depends(get_current_user),
):
    user = service.get_user(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.put("/users/{user_id}", response_model=UserRead)
def update_user(
    user_id: int,
    user: UserUpdate,
    service: UserService = Depends(get_user_service),
    _: UserORM = Depends(get_current_user),
):
    updated = service.update_user(
        user_id,
        username=user.username,
        password=user.password,
        email=user.email,
        full_name=user.full_name,
    )
    if not updated:
        raise HTTPException(status_code=404, detail="User not found")
    return updated


@router.delete("/users/{user_id}")
def delete_user(
    user_id: int,
    service: UserService = Depends(get_user_service),
    current_user: UserORM = Depends(get_current_user),
):
    if not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Admin access required")
    success = service.delete_user(user_id)
    if not success:
        raise HTTPException(status_code=404, detail="User not found")
    return {"success": True}
