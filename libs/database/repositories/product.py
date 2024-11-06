from typing import Union, Dict, Any, Optional
from uuid import UUID

from elasticsearch import AsyncElasticsearch
from sqlalchemy.ext.asyncio import AsyncSession

from libs.database.models import Product
from libs.database.repositories.base import BaseRepository
from libs.elastic.repository import ElasticRepository


class ProductRepository(BaseRepository[Product], ElasticRepository[Product]):
    def __init__(self, session: AsyncSession, es_client: AsyncElasticsearch):
        BaseRepository.__init__(self, Product, session)
        ElasticRepository.__init__(self, Product, es_client, index_name="products")

    async def add(self, entity: Product):
        """
        Добавляет продукт в базу данных и индексирует в Elastic.

        :param entity: Модель продукта.
        """
        await super().add(entity)
        await self.index_entity(entity)

    async def update(self, entity_id: Union[int, UUID], data: Union[Product, Dict[str, Any]]):
        """
        Обновляет продукт в базе данных и синхронизирует Elastic.

        :param entity_id: Идентификатор записи, которую нужно обновить.
        :param data: Словарь с данными для обновления (имена полей и новые значения) или изменённая модель.
        """
        await super().update(entity_id, data)
        updated_product = await self.get(entity_id)
        if updated_product:
            await self.index_entity(updated_product)

    async def delete(self, entity_id: Union[int, UUID]):
        """
        Удаляет продукт из базы данных и его индекс в Elastic.

        :param entity_id: Идентификатор записи, которую нужно удалить.
        """
        await super().delete(entity_id)
        await self.delete_entity(entity_id)

    async def search_products(self, query: str, limit: int, filters: Dict[str, Any] = None, sort: Optional[str] = None,
                              cursor: Optional[str] = None):
        """
        Поиск продуктов с фильтрацией и пагинацией.

        :param query: Поисковый запрос.
        :param limit: Количество записей на странице.
        :param filters: Фильтры для поиска.
        :param sort: Поле для сортировки.
        :param cursor: Значение курсора для пагинации.
        """
        return await self.search(["title", "description"], query, limit, filters, sort, cursor)
