from sqlmodel.ext.asyncio.session import AsyncSession

from libs.database.models import Order
from libs.database.repositories import BaseRepository


class OrderRepository(BaseRepository[Order]):
    def __init__(self, session: AsyncSession):
        super().__init__(Order, session)
