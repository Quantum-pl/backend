from sqlalchemy.ext.asyncio import AsyncSession

from app.database.models import Session
from app.database.repositories.base import BaseRepository


class SessionRepository(BaseRepository[Session]):
    def __init__(self, session: AsyncSession):
        super().__init__(Session, session)