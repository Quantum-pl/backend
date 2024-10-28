from typing import Optional, List

from sqlmodel.ext.asyncio.session import AsyncSession

from libs.database.models import Verification
from libs.database.repositories import BaseRepository


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

    async def get_by_token(self, token: str, relations: Optional[List[str]] = None) -> Optional[Verification]:
        """
        Ищет запись в таблице Verification по значению токена.

        :param token: Значение токена для поиска записи.
        :param relations: Список имен связанных сущностей для предварительной загрузки.
        :return: Объект Session или None, если запись не найдена.
        """
        return await self.get_by_field("token", token, relations)
