import enum
import uuid

from app.database.models import Base, User, Order
from app.database.models.order import order_products

from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey, Enum, Table
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship, Mapped


class ProductState(enum.Enum):
    ACTIVE = "ACTIVE"
    DISABLED = "DISABLED"
    OUT_OF_STOCK = "OUT_OF_STOCK"

class Product(Base):
    __tablename__ = 'products'

    id: Mapped[int] = Column(Integer, primary_key=True)

    title: Mapped[str] = Column(String, nullable=False)
    body: Mapped[str] = Column(Text, nullable=False)
    price: Mapped[int] = Column(Integer)

    status: Mapped[ProductState] = Column(Enum(ProductState), default=ProductState.ACTIVE)
    created_at: Mapped[datetime] = Column(DateTime, default=datetime.now)

    user: Mapped["User"] = relationship("User", back_populates="products")
    orders: Mapped[list["Order"]] = relationship("Order", secondary=order_products, back_populates="products")

    def __repr__(self):
        return f"<Product(id={self.id}, title={self.title}, price={self.price})>"