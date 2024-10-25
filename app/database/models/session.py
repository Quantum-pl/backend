import uuid
from datetime import datetime
from typing import TYPE_CHECKING

from app.database.models import Base, User

from sqlalchemy import Column, Integer, String, DateTime, UUID, ForeignKey
from sqlalchemy.orm import Mapped, relationship


if TYPE_CHECKING:
    from .user import User

class Session(Base):
    __tablename__ = 'sessions'

    id: Mapped[int] = Column(Integer, primary_key=True)
    token: Mapped[str] = Column(String)
    refresh: Mapped[str] = Column(String)

    created_at: Mapped[datetime] = Column(DateTime, default=datetime.now)
    expire_at: Mapped[datetime] = Column(DateTime)

    user_id: Mapped[uuid.UUID] = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    user: Mapped["User"] = relationship("User", back_populates="products")

    def __repr__(self):
        return f"<Session(id={self.id}, user_id={self.user_id})>"
