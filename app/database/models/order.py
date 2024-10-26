import uuid
from datetime import datetime
from enum import Enum
from typing import List, Optional, TYPE_CHECKING

from sqlmodel import SQLModel, Field, Relationship

from .links import OrderProductLink

if TYPE_CHECKING:
    from app.database.models.user import User
    from app.database.models.product import Product


class OrderState(str, Enum):
    PENDING = "PENDING"
    CREATED = "CREATED"
    ACCEPTED = "ACCEPTED"
    IN_TRANSIT = "IN_TRANSIT"
    DELIVERED = "DELIVERED"


class Order(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    status: OrderState = Field(default=OrderState.CREATED)
    created_at: datetime = Field(default_factory=datetime.now)
    user_id: uuid.UUID = Field(foreign_key="user.id")

    user: Optional["User"] = Relationship(back_populates="orders")
    products: List["Product"] = Relationship(back_populates="orders", link_model=OrderProductLink)
