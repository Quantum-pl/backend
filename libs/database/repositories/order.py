from sqlmodel.ext.asyncio.session import AsyncSession

from libs.database.models import Order
from libs.database.repositories import BaseRepository


class OrderRepository(BaseRepository[Order]):
    def __init__(self, session: AsyncSession):
        super().__init__(Order, session)

    async def get_user_orders(self, user_id: int):
        return await self.session.exec(self.model.select().where(self.model.user_id == user_id))
