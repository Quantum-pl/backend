import uuid
from datetime import datetime
from enum import Enum
from typing import TYPE_CHECKING, Optional

from sqlmodel import SQLModel, Field, Relationship

if TYPE_CHECKING:
    from .user import User


class VerificationType(str, Enum):
    EMAIL = "EMAIL"
    PASSWORD_RESET = "PASSWORD_RESET"


class Verification(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: uuid.UUID = Field(foreign_key="users.id")

    type: VerificationType
    verification_code: str

    created_at: datetime = Field(default_factory=datetime.now)
    expire_at: datetime

    user: Optional["User"] = Relationship(back_populates="verifications")
