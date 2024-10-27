import uuid
from datetime import datetime
from enum import Enum
from typing import List, Optional, TYPE_CHECKING

from sqlmodel import SQLModel, Field, Relationship

from .links import OrderProductLink

if TYPE_CHECKING:
    from .user import User
    from .order import Order


class ProductState(str, Enum):
    ACTIVE = "ACTIVE"
    DISABLED = "DISABLED"
    OUT_OF_STOCK = "OUT_OF_STOCK"


class Product(SQLModel, table=True):
    __tablename__ = 'products'

    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: uuid.UUID = Field(foreign_key="users.id")

    title: str
    body: str
    price: Optional[int]
    status: ProductState = Field(default=ProductState.ACTIVE)
    created_at: datetime = Field(default_factory=datetime.now)

    user: Optional["User"] = Relationship(back_populates="products")
    orders: List["Order"] = Relationship(back_populates="products", link_model=OrderProductLink)
