import enum

from typing import TYPE_CHECKING
from app.database.models import Base, User

from sqlalchemy import Column, Integer, ForeignKey, String, Enum, UUID
from sqlalchemy.orm import Mapped, relationship


if TYPE_CHECKING:
    from .user import User

class VerificationType(enum.Enum):
    EMAIL = "EMAIL"
    PASSWORD_RESET = "PASSWORD_RESET"


class Verification(Base):
    __tablename__ = 'verifications'

    id: Mapped[int] = Column(Integer, primary_key=True)
    type: Mapped[VerificationType] = Column(Enum(VerificationType), nullable=False)
    token: Mapped[str] = Column(String, nullable=False)

    user: Mapped["User"] = relationship("User", back_populates="products")

    def __repr__(self):
        return f"<Verification(id={self.id}, token={self.token})>"