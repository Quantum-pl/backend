import uuid
from enum import Enum
from typing import Optional, Dict, Any, List

from pydantic import BaseModel, Field


class ProductState(str, Enum):
    ACTIVE = "ACTIVE"
    DISABLED = "DISABLED"
    OUT_OF_STOCK = "OUT_OF_STOCK"


class ProductBase(BaseModel):
    title: str = Field(..., max_length=255)
    description: str
    price: int


class ProductCreate(ProductBase):
    """Схема для создания продукта."""


class ProductUpdate(BaseModel):
    """Схема для обновления продукта."""
    title: Optional[str] = Field(None, max_length=255)
    description: Optional[str]
    price: Optional[int]


class ProductSearchRequest(BaseModel):
    """Схема для запроса поиска продуктов."""
    query: Optional[str] = None
    limit: Optional[int] = 10
    cursor: Optional[str] = None

    filters: Optional[Dict[str, Any]] = None
    sort: Optional[List[str]] = None


class ProductResponse(ProductBase):
    """Схема для ответа при запросе продукта."""
    id: uuid.UUID
    status: ProductState

    class Config:
        orm_mode = True
