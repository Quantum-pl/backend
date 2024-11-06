from typing import Type, TypeVar, Generic, Dict, Any, List, Optional, Union
from uuid import UUID

from elasticsearch import AsyncElasticsearch
from sqlmodel import SQLModel

T = TypeVar("T", bound=SQLModel)


class ElasticRepository(Generic[T]):
    def __init__(self, model: Type[T], es_client: AsyncElasticsearch, index_name: str):
        self.model = model
        self.es_client = es_client
        self.index_name = index_name

    async def index_entity(self, entity: T):
        """Индексация сущности в Elasticsearch."""
        doc = self._map_to_document(entity)
        await self.es_client.index(index=self.index_name, id=str(entity.id), body=doc)

    async def delete_entity(self, entity_id: Union[int, UUID]):
        """Удаляет документ из индекса Elasticsearch по ID."""
        await self.es_client.delete(index=self.index_name, id=str(entity_id))

    async def search(
            self,
            fields: List[str],
            query: str = "",
            limit: Optional[int] = None,
            filters: Optional[Dict[str, Any]] = None,
            sort: Optional[List[str]] = None,
            cursor: Optional[str] = None
    ) -> List[T]:
        """Поиск сущностей в Elasticsearch по запросу, фильтрам и пагинации."""
        must_conditions = [{"multi_match": {"query": query, "fields": fields}}] if query else []
        filter_conditions = [{"term": {k: v}} for k, v in (filters or {}).items()]

        sort_order = sort if sort else [{"_doc": "asc"}]

        # Убираем параметр search_after, если cursor None
        search_query = {
            "query": {
                "bool": {
                    "must": must_conditions,
                    "filter": filter_conditions
                }
            },
            "size": limit,
            "sort": sort_order
        }

        if cursor:
            search_query["search_after"] = cursor

        response = await self.es_client.search(index=self.index_name, body=search_query)
        return [self._map_to_entity(hit["_source"]) for hit in response["hits"]["hits"]]

    def _map_to_document(self, entity: T) -> Dict[str, Any]:
        """Преобразует объект SQLModel в документ Elasticsearch."""
        return entity.model_dump(exclude={"id"})

    def _map_to_entity(self, source: Dict[str, Any]) -> T:
        """Преобразует документ Elasticsearch в объект модели SQLModel."""
        return self.model(**source)
