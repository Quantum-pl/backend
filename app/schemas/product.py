from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field


class ProductState(str, Enum):
    ACTIVE = "ACTIVE"
    DISABLED = "DISABLED"
    OUT_OF_STOCK = "OUT_OF_STOCK"


class ProductBase(BaseModel):
    title: str = Field(..., max_length=255)
    body: str
    price: int


class ProductCreate(ProductBase):
    """Схема для создания продукта."""
    status: Optional[ProductState] = ProductState.ACTIVE


class ProductUpdate(BaseModel):
    """Схема для обновления продукта."""
    title: Optional[str] = Field(None, max_length=255)
    body: Optional[str]
    price: Optional[int]
    status: Optional[ProductState]


class ProductResponse(ProductBase):
    """Схема для ответа при запросе продукта."""
    id: int
    status: ProductState

    class Config:
        orm_mode = True
