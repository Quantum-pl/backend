from typing import Type, TypeVar, Generic, Dict, Any, Optional, List, Union
from uuid import UUID

from sqlmodel import SQLModel, select, update, delete
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import selectinload

T = TypeVar("T", bound=SQLModel)


class BaseRepository(Generic[T]):
    """
    Базовый репозиторий для работы с базовыми операциями CRUD для моделей SQLModel.
    """

    def __init__(self, model: Type[T], session: AsyncSession):
        """
        Инициализирует репозиторий с моделью и сессией.

        :param model: Класс модели, связанный с этим репозиторием.
        :param session: Асинхронная сессия для работы с базой данных.
        """
        self.model = model
        self.session = session

    async def add(self, entity: T) -> None:
        """
        Добавляет новую запись в базу данных и выполняет коммит.

        :param entity: Экземпляр модели, который нужно сохранить.
        """
        try:
            self.session.add(entity)
            await self.session.commit()
        except IntegrityError:
            await self.session.rollback()

    async def get(self, entity_id: Union[int, UUID], relations: Optional[List[str]] = None) -> Optional[T]:
        """
        Получает запись из базы данных по ID.

        :param entity_id: Идентификатор записи, которую нужно получить.
        :param relations: Список имен связанных сущностей для предварительной загрузки.
        :return: Объект модели или None, если запись не найдена.
        """
        query = select(self.model).where(self.model.id == entity_id)

        if relations:
            for relation in relations:
                query = query.options(selectinload(getattr(self.model, relation)))

        result = await self.session.exec(query)
        return result.one_or_none()  # Получаем одну запись или None

    async def get_all(
            self,
            filters: Optional[Dict[str, Any]] = None,
            relations: Optional[List[str]] = None,
            limit: Optional[int] = None,
            offset: Optional[int] = None
    ) -> List[T]:
        """
        Получает список всех записей из базы данных с опциональными фильтрами и связями.

        :param filters: Словарь с полями и значениями для фильтрации записей.
        :param relations: Список имен связанных сущностей для предварительной загрузки.
        :param limit: Лимит записей, которые нужно вернуть.
        :param offset: Смещение записей для пагинации.
        :return: Список объектов модели, удовлетворяющих фильтрам.
        """
        query = select(self.model)

        if filters:
            for field_name, value in filters.items():
                query = query.where(getattr(self.model, field_name) == value)

        if relations:
            for relation in relations:
                query = query.options(selectinload(getattr(self.model, relation)))

        if limit:
            query = query.limit(limit)

        if offset:
            query = query.offset(offset)

        result = await self.session.exec(query)
        return result.all()

    async def get_by_field(self, field_name: str, value: Any, relations: Optional[List[str]] = None) -> Optional[T]:
        """
        Получает запись из базы данных по произвольному полю и значению.

        :param field_name: Имя поля, по которому будет выполнен запрос.
        :param value: Значение, по которому производится поиск.
        :param relations: Список имен связанных сущностей для предварительной загрузки.
        :return: Объект модели или None, если запись не найдена.
        """
        query = select(self.model).where(getattr(self.model, field_name) == value)

        if relations:
            for relation in relations:
                query = query.options(selectinload(getattr(self.model, relation)))

        result = await self.session.exec(query)
        return result.one_or_none()

    async def update(self, entity_id: Union[int, UUID], data: Dict[str, Any]) -> None:
        """
        Обновляет запись в базе данных по ID, изменяя указанные поля.

        :param entity_id: Идентификатор записи, которую нужно обновить.
        :param data: Словарь с данными для обновления (имена полей и новые значения).
        """
        await self.session.exec(
            update(self.model)
            .where(self.model.id == entity_id)
            .values(**data)
        )
        await self.session.commit()

    async def delete(self, entity_id: Union[int, UUID]) -> None:
        """
        Удаляет запись из базы данных по ID.

        :param entity_id: Идентификатор записи, которую нужно удалить.
        """
        await self.session.exec(
            delete(self.model).where(self.model.id == entity_id)
        )
        await self.session.commit()
