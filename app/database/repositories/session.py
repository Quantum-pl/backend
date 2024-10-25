from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.models import Session
from app.database.repositories.base import BaseRepository

class SessionRepository(BaseRepository[Session]):
    """
    Репозиторий для работы с записями модели Session.
    """

    def __init__(self, session: AsyncSession):
        super().__init__(Session, session)

    async def get_by_refresh_token(self, refresh_token: str) -> Optional[Session]:
        """
        Ищет запись в таблице Session по значению токена обновления.

        :param refresh_token: Значение токена обновления для поиска записи.
        :return: Объект Session или None, если запись не найдена.
        """
        return await self.get_by_field("refresh", refresh_token)

    async def get_by_token(self, token: str) -> Optional[Session]:
        """
        Ищет запись в таблице Session по значению токена.

        :param token: Значение токена для поиска записи.
        :return: Объект Session или None, если запись не найдена.
        """
        return await self.get_by_field("token", token)
