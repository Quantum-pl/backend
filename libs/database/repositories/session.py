from typing import Optional, List

from sqlmodel.ext.asyncio.session import AsyncSession

from libs.database.models import Session
from libs.database.repositories import BaseRepository


class SessionRepository(BaseRepository[Session]):
    """
    Репозиторий для работы с записями модели Session.
    """

    def __init__(self, session: AsyncSession):
        super().__init__(Session, session)

    async def get_by_refresh_token(self, refresh_token: str, relations: Optional[List[str]] = None) -> Optional[
        Session]:
        """
        Ищет запись в таблице Session по значению токена обновления.

        :param refresh_token: Значение токена обновления для поиска записи.
        :param relations: Список имен связанных сущностей для предварительной загрузки.
        :return: Объект Session или None, если запись не найдена.
        """
        return await self.get_by_field("refresh", refresh_token, relations)

    async def get_by_access_token(self, token: str, relations: Optional[List[str]] = None) -> Optional[Session]:
        """
        Ищет запись в таблице Session по значению токена.

        :param token: Значение токена для поиска записи.
        :param relations: Список имен связанных сущностей для предварительной загрузки.
        :return: Объект Session или None, если запись не найдена.
        """
        return await self.get_by_field("access_token", token, relations)
