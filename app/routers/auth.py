import uuid
import bcrypt
import secrets
from datetime import datetime, timedelta
from fastapi import APIRouter, HTTPException, status, Response, Cookie

from app.database.session import SessionDep
from app.database.models import Session
from app.database.repositories.user import UserRepository
from app.database.repositories.session import SessionRepository
from app.schemas import LoginRequest

router = APIRouter(
    prefix="/auth",
    tags=["auth"],
)

def hash_token(token: str) -> str:
    """Хэширует токен с использованием bcrypt.

    :param token: Токен, который нужно хэшировать.
    :return: Хэшированный токен.
    """
    return bcrypt.hashpw(token.encode(), bcrypt.gensalt()).decode()

def verify_token(token: str, hashed_token: str) -> bool:
    """Проверяет, совпадает ли токен с хэшированной версией.

    :param token: Оригинальный токен для проверки.
    :param hashed_token: Хэшированный токен для сравнения.
    :return: True, если токены совпадают; иначе False.
    """
    return bcrypt.checkpw(token.encode(), hashed_token.encode())

async def create_session(user_id: uuid.UUID, session_repo: SessionRepository) -> (str, str):
    """Создаёт новую сессию с хэшированным токеном и сроком действия.

    :param user_id: Идентификатор пользователя, для которого создается сессия.
    :param session_repo: Репозиторий для работы с сессиями.
    :return: Токен и refresh-токен для новой сессии.
    """
    token = secrets.token_urlsafe(32)
    refresh_token = secrets.token_urlsafe(32)

    hashed_token = hash_token(token)
    hashed_refresh_token = hash_token(refresh_token)

    new_session = Session(
        token=hashed_token,
        refresh=hashed_refresh_token,
        user_id=user_id,
        created_at=datetime.now(),
        expire_at=datetime.now() + timedelta(days=7)
    )

    await session_repo.add(new_session)
    return token, refresh_token

@router.post("/login")
async def login(login_data: LoginRequest, db: SessionDep, response: Response):
    """Выполняет вход пользователя, создаёт сессию и возвращает токены."""
    user_repo = UserRepository(db)
    session_repo = SessionRepository(db)

    user = await user_repo.get_by_field("email", login_data.email)

    if user is None or not user.password == login_data.password:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

    token, refresh_token = await create_session(user.id, session_repo)
    response.set_cookie(key="access_token", value=token, httponly=True, secure=True, samesite="lax")
    response.set_cookie(key="refresh_token", value=refresh_token, httponly=True, secure=True, samesite="lax")
    return {"message": "Successfully logged in"}

@router.post("/refresh")
async def refresh_token(response: Response, db: SessionDep, refresh_token: str = Cookie(...)):
    """Обновляет токен сессии, если токен обновления действителен."""
    session_repo = SessionRepository(db)
    session = await session_repo.get_by_refresh_token(refresh_token)

    if session is None or session.expire_at < datetime.now():
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Session expired")

    new_token = secrets.token_urlsafe(32)
    new_refresh_token = secrets.token_urlsafe(32)
    await session_repo.update(session.id, {
        "token": hash_token(new_token),
        "refresh": hash_token(new_refresh_token),
        "expire_at": datetime.now() + timedelta(days=7)
    })

    response.set_cookie(key="access_token", value=new_token, httponly=True, secure=True, samesite="lax")
    response.set_cookie(key="refresh_token", value=new_refresh_token, httponly=True, secure=True, samesite="lax")
    return {"message": "Successfully refreshed"}

@router.post("/logout")
async def logout(token: str, db: SessionDep, response: Response):
    """Удаляет сессию пользователя при выходе из системы."""
    session_repo = SessionRepository(db)
    session = await session_repo.get_by_token(token)

    if session is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Session not found")

    await session_repo.delete(session.id)
    response.delete_cookie(key="access_token")
    response.delete_cookie(key="refresh_token")
    return {"message": "Successfully logged out"}
