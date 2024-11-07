import asyncio
from concurrent.futures import ThreadPoolExecutor
from typing import Annotated, List, Set, Any

from elasticsearch import AsyncElasticsearch
from elasticsearch.helpers import async_bulk
from fastapi import Depends
from sqlmodel.ext.asyncio.session import AsyncSession

from app.config import settings
from libs.database.models import Product
from libs.database.repositories import ProductRepository

es_client = AsyncElasticsearch(str(settings.elastic_url))


async def get_es_client():
    yield es_client

async def sync_elasticsearch(db_session: AsyncSession, index_name: str, index_settings: dict[str, Any]) -> None:
    """
    Синхронизирует продукты из базы данных с Elasticsearch,
    добавляя или обновляя новые записи и удаляя записи, которых нет в базе данных.
    Также проверяет и создает индекс, если его нет.
    """

    if not await es_client.indices.exists(index=index_name):
        await es_client.indices.create(index=index_name, body=index_settings)

    product_repo = ProductRepository(db_session, es_client)
    products: List[Product] = await product_repo.get_all()

    db_product_ids: Set[str] = {str(product.id) for product in products}
    es_product_ids = await get_all_indexed_ids(es_client, index_name=index_name)

    products_to_index = []
    products_to_delete = []

    for product in products:
        products_to_index.append({
            "_op_type": "index",
            "_index": index_name,
            "_id": str(product.id),
            "_source": product.model_dump(exclude={"id"})
        })

    for product_id in es_product_ids - db_product_ids:
        products_to_delete.append({
            "_op_type": "delete",
            "_index": index_name,
            "_id": product_id
        })

    tasks = []

    if products_to_index:
        tasks.append(async_bulk(es_client, products_to_index))

    if products_to_delete:
        tasks.append(async_bulk(es_client, products_to_delete))

    if tasks:
        await asyncio.gather(*tasks)


async def get_all_indexed_ids(es_client: AsyncElasticsearch, index_name: str) -> Set[str]:
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
