import hashlib
import hmac
import secrets
import uuid
from datetime import datetime, timedelta

from app.config import settings
from app.database.models import Session
from app.database.repositories import SessionRepository


def hash_token(token: str) -> str:
    """Хэширует токен с использованием hmac.

    :param token: Токен, который нужно хэшировать.
    :return: Хэшированный токен.
    """
    return hmac.new(settings.secret_key.encode(), token.encode(), hashlib.sha256).hexdigest()


def verify_token(token: str, hashed_token: str) -> bool:
    """Проверяет, совпадает ли токен с хэшированной версией.

    :param token: Оригинальный токен для проверки.
    :param hashed_token: Хэшированный токен для сравнения.
    :return: True, если токены совпадают; иначе False.
    """
    return hmac.compare_digest(hash_token(token), hashed_token)


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
        access_token=hashed_token,
        refresh_token=hashed_refresh_token,
        user_id=user_id,
        created_at=datetime.now(),
        expire_at=datetime.now() + timedelta(days=7)
    )

    await session_repo.add(new_session)
    return token, refresh_token
