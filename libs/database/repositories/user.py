from sqlmodel.ext.asyncio.session import AsyncSession

from libs.database.models import User
from libs.database.repositories import BaseRepository


class UserRepository(BaseRepository[User]):
    def __init__(self, session: AsyncSession):
        super().__init__(User, session)
