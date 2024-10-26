from typing import Optional

from sqlmodel.ext.asyncio.session import AsyncSession

from app.database.models import Verification
from app.database.repositories.base import BaseRepository


class VerificationRepository(BaseRepository[Verification]):
    """
    Репозиторий для работы с записями модели Verification.
    """

    def __init__(self, session: AsyncSession):
        """
        Инициализирует репозиторий Verification с асинхронной сессией.

        :param session: Асинхронная сессия для работы с базой данных.
        """
        super().__init__(Verification, session)

    async def get_by_token(self, token: str) -> Optional[Verification]:
        """
        Ищет запись в таблице Verification по значению токена.

        :param token: Значение токена для поиска записи.
        :return: Объект Verification или None, если запись не найдена.
        """
        return await self.get_by_field("token", token)
