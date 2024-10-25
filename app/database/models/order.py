import enum
import uuid

from datetime import datetime
from app.database.models import Base, User, Product
from sqlalchemy import Column, Integer, DateTime, Enum, UUID, ForeignKey, Table
from sqlalchemy.orm import Mapped, relationship

order_products = Table(
    "order_products", Base.metadata,
    Column("order_id", ForeignKey("orders.id"), primary_key=True),
    Column("product_id", ForeignKey("products.id"), primary_key=True)
)

class OrderState(enum.Enum):
    PENDING = enum.auto()
    CREATED = enum.auto()
    ACCEPTED = enum.auto()
    IN_TRANSIT = enum.auto()
    DELIVERED = enum.auto()


class Order(Base):
    __tablename__ = 'orders'

    id: Mapped[int] = Column(Integer, primary_key=True)
    user_id: Mapped[uuid.UUID] = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    status: Mapped[OrderState] = Column(Enum(OrderState), default=OrderState.CREATED)

    created_at: Mapped[datetime] = Column(DateTime, default=datetime.utcnow)

    user: Mapped["User"] = relationship("User", back_populates="orders")
    products: Mapped[list["Product"]] = relationship("Product", secondary=order_products, back_populates="orders")

    def __repr__(self):
        return f"<Order(id={self.id}, user_id={self.user_id}, status={self.status})>"
