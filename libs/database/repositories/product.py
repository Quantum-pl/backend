from sqlmodel.ext.asyncio.session import AsyncSession

from libs.database.models import Product
from libs.database.repositories import BaseRepository


class ProductRepository(BaseRepository[Product]):
    def __init__(self, session: AsyncSession):
        super().__init__(Product, session)
