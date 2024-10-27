import uuid

from fastapi import APIRouter, HTTPException, status

from app.database.engine import SessionDep
from app.database.repositories import UserRepository
from app.middleware.auth import AuthMiddlewareDep
from app.schemas.user import UserRead

router = APIRouter(
    prefix="/users",
    tags=["users"]
)


@router.get("/me", response_model=UserRead)
async def read_user_me(
        current_user: AuthMiddlewareDep
):
    """
    Возвращает информацию о текущем авторизованном пользователе.
    """
    return current_user


@router.get("/{id}", response_model=UserRead)
async def read_user(id: uuid.UUID, session: SessionDep):
    """
    Находит и возвращает информацию о пользователе по имени пользователя.
    """
    user_repo = UserRepository(session)
    user = await user_repo.get(id)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    return user
