import secrets
import uuid
from datetime import datetime, timedelta

from fastapi import APIRouter, HTTPException, status, Response, Cookie

from app.schemas.auth import RegisterRequest, LoginRequest
from app.utils.auth import hash_token, verify_token, create_session
from libs.database import SessionDep
from libs.database.models import User
from libs.database.repositories import UserRepository, SessionRepository

router = APIRouter(
    prefix="/auth",
    tags=["auth"],
)


@router.post("/register")
async def register(register_data: RegisterRequest, response: Response, db: SessionDep):
    """Регистрирует нового пользователя, создаёт сессию и возвращает оригинальные токены."""
    user_repo = UserRepository(db)
    session_repo = SessionRepository(db)

    existing_user = await user_repo.get_by_field("email", register_data.email)
    if existing_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User already exists")

    new_user = User(
        id=uuid.uuid4(),
        email=register_data.email,
        password=hash_token(register_data.password),
        first_name=register_data.first_name,
        last_name=register_data.last_name,
        created_at=datetime.now(),
    )

    try:
        await user_repo.add(new_user)
    except:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User cannot create")

    token, refresh_token = await create_session(new_user.id, session_repo)
    response.set_cookie(key="access_token", value=token, httponly=True, secure=True, samesite="lax")
    response.set_cookie(key="refresh_token", value=refresh_token, httponly=True, secure=True, samesite="lax")
    return {"message": "Successfully registered"}


@router.post("/login")
async def login(login_data: LoginRequest, response: Response, db: SessionDep):
    """Выполняет вход пользователя, создаёт сессию и возвращает токены."""
    user_repo = UserRepository(db)
    session_repo = SessionRepository(db)
    user = await user_repo.get_by_field("email", login_data.email)

    if user is None or not verify_token(login_data.password, user.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

    token, refresh_token = await create_session(user.id, session_repo)
    response.set_cookie(key="access_token", value=token, httponly=True, secure=True, samesite="lax")
    response.set_cookie(key="refresh_token", value=refresh_token, httponly=True, secure=True, samesite="lax")
    return {"message": "Successfully logged in"}


@router.post("/refresh")
async def refresh(response: Response, db: SessionDep, refresh_token: str = Cookie(...)):
    """Обновляет токен сессии, если токен обновления действителен."""
    session_repo = SessionRepository(db)
    session = await session_repo.get_by_refresh_token(refresh_token)

    if session is None or session.expire_at < datetime.now():
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Session expired")

    new_token = secrets.token_urlsafe(32)
    new_refresh_token = secrets.token_urlsafe(32)
    await session_repo.update(session.id, {
        "access_token": hash_token(new_token),
        "refresh_token": hash_token(new_refresh_token),
        "expire_at": datetime.now() + timedelta(days=7)
    })

    response.set_cookie(key="access_token", value=new_token, httponly=True, secure=True, samesite="lax")
    response.set_cookie(key="refresh_token", value=new_refresh_token, httponly=True, secure=True, samesite="lax")
    return {"message": "Successfully refreshed"}


@router.post("/logout")
async def logout(response: Response, db: SessionDep, access_token: str = Cookie(...)):
    """Удаляет сессию пользователя при выходе из системы."""
    session_repo = SessionRepository(db)
    session = await session_repo.get_by_token(access_token)

    if session is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Session not found")

    await session_repo.delete(session.id)
    response.delete_cookie(key="access_token")
    response.delete_cookie(key="refresh_token")

    return {"message": "Successfully logged out"}
