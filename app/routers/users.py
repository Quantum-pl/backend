import uuid
from datetime import datetime
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, status, Cookie

from app.database.engine import SessionDep
from app.database.models import User
from app.database.repositories import UserRepository, SessionRepository

router = APIRouter(
    prefix="/users",
    tags=["users"]
)


async def get_current_user(session: SessionDep, access_token: str = Cookie(...)) -> Optional[User]:
    """
    Проверяет токен, чтобы найти и вернуть текущего пользователя.
    """
    session_repo = SessionRepository(session)

    db_session = await session_repo.get_by_token(access_token)
    if db_session is None or db_session.expire_at < datetime.now():
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token"
        )

    user_repo = UserRepository(session)
    user = await user_repo.get(db_session.user_id)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    return user


@router.get("/me")
async def read_user_me(
        current_user: User = Depends(get_current_user)
):
    """
    Возвращает информацию о текущем авторизованном пользователе.
    """
    return {"username": current_user.nickname, "email": current_user.email}


@router.get("/{id}")
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

    return {"username": user.nickname}
