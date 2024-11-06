import uuid

from fastapi import Request, APIRouter, HTTPException, status

from app.middleware.auth import authorize
from app.schemas.user import UserRead
from libs.database.repositories import UserRepository

router = APIRouter(
    prefix="/users",
    tags=["users"]
)


@router.get("/me", response_model=UserRead)
@authorize()
async def read_user_me(request: Request):
    """
    Возвращает информацию о текущем авторизованном пользователе.
    """

    return request.state.current_user


@router.get("/{id}", response_model=UserRead)
async def read_user(id: uuid.UUID, request: Request):
    """
    Находит и возвращает информацию о пользователе по имени пользователя.
    """
    user_repo = UserRepository(request.state.db)
    user = await user_repo.get(id)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    return user
