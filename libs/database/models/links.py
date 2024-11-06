import uuid
from typing import Optional

from sqlmodel import SQLModel, Field


class OrderProductLink(SQLModel, table=True):
    __tablename__ = 'order_products'
    order_id: Optional[uuid.UUID] = Field(default=None, foreign_key="orders.id", primary_key=True)
    product_id: Optional[uuid.UUID] = Field(default=None, foreign_key="products.id", primary_key=True)
