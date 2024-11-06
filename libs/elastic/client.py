from typing import Annotated, List, Set

from elasticsearch import AsyncElasticsearch
from fastapi import Depends
from sqlmodel.ext.asyncio.session import AsyncSession

from app.config import settings
from libs.database.models import Product
from libs.database.repositories import ProductRepository

es_client = AsyncElasticsearch(str(settings.elastic_url))


async def get_es_client():
    yield es_client


async def sync_elasticsearch(db_session: AsyncSession, index_name: str = "products"):
    """
    Синхронизирует продукты из базы данных с Elasticsearch,
    добавляя или обновляя новые записи и удаляя записи, которых нет в базе данных.
    Также проверяет и создает индекс, если его нет.
    """

    if not await es_client.indices.exists(index=index_name):
        await es_client.indices.create(index=index_name)

    product_repo = ProductRepository(db_session, es_client)
    products: List[Product] = await product_repo.get_all()
    db_product_ids: Set[str] = {str(product.id) for product in products}

    es_product_ids = await get_all_indexed_ids(es_client, index_name=index_name)

    for product in products:
        await product_repo.index_entity(product)

    ids_to_delete = es_product_ids - db_product_ids
    for product_id in ids_to_delete:
        await product_repo.delete_entity(int(product_id))



async def get_all_indexed_ids(es_client, index_name) -> Set[str]:
    query = {
        "query": {
            "match_all": {}
        },
        "size": 1000
    }

    all_ids = set()
    response = await es_client.search(index=index_name, body=query)

    while True:
        all_ids.update(hit["_id"] for hit in response["hits"]["hits"])

        if len(response["hits"]["hits"]) < 1000:
            break

        query["search_after"] = response["hits"]["hits"][-1]["sort"]
        response = await es_client.search(index=index_name, body=query)

    return all_ids



ElasticDep = Annotated[AsyncElasticsearch, Depends(get_es_client)]
