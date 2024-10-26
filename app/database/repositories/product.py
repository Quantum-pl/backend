from sqlmodel.ext.asyncio.session import AsyncSession

from app.database.models import Product
from app.database.repositories.base import BaseRepository


class ProductRepository(BaseRepository[Product]):
    def __init__(self, session: AsyncSession):
        super().__init__(Product, session)
