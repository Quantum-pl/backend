from datetime import datetime
from enum import Enum
from typing import List, Optional
from uuid import UUID

from pydantic import BaseModel


class OrderState(str, Enum):
    PENDING = "PENDING"
    CREATED = "CREATED"
    ACCEPTED = "ACCEPTED"
    IN_TRANSIT = "IN_TRANSIT"
    DELIVERED = "DELIVERED"


class OrderBase(BaseModel):
    user_id: UUID


class OrderCreate(OrderBase):
    """Схема для создания заказа."""
    products: List[int]


class OrderUpdate(BaseModel):
    """Схема для обновления заказа."""
    status: Optional[OrderState]
    products: Optional[List[int]]


class OrderResponse(OrderBase):
    """Схема для ответа при запросе заказа."""
    id: int
    status: OrderState
    created_at: datetime
    products: List[int]

    class Config:
        orm_mode = True
