from sqlalchemy.ext.asyncio import AsyncSession

from app.database.models import User
from app.database.repositories.base import BaseRepository


class UserRepository(BaseRepository[User]):
    def __init__(self, session: AsyncSession):
        super().__init__(User, session)
