import uuid

from datetime import datetime
from typing import TYPE_CHECKING

from app.database.models import Base

from sqlalchemy.orm import Mapped, relationship
from sqlalchemy import Column, Integer, String, Boolean, DateTime, UUID


if TYPE_CHECKING:
    from .order import Order
    from .product import Product
    from .session import Session

class User(Base):
    __tablename__ = 'users'

    id: Mapped[uuid.UUID] = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    avatar: Mapped[str] = Column(String)
    email: Mapped[str] = Column(String(225), nullable=False, unique=True)
    phone: Mapped[str] = Column(String, unique=True)
    password: Mapped[str] = Column(String, nullable=False)
    nickname: Mapped[str] = Column(String, nullable=False)
    isEmailVerified: Mapped[bool] = Column(Boolean, default=False)
    flags: Mapped[int] = Column(Integer, default=0)

    created_at: Mapped[datetime] = Column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = Column(DateTime, onupdate=datetime.utcnow)

    sessions: Mapped[list["Session"]] = relationship("Session", back_populates="user")
    products: Mapped[list["Product"]] = relationship("Product", back_populates="user")
    orders: Mapped[list["Order"]] = relationship("Order", back_populates="user")

    def __repr__(self):
        return f"<User(id={self.id}, email={self.email})>"
