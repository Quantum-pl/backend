from typing import TYPE_CHECKING, Optional
from sqlmodel import SQLModel, Field, Relationship
from enum import Enum
import uuid

if TYPE_CHECKING:
    from .user import User


class VerificationType(str, Enum):
    EMAIL = "EMAIL"
    PASSWORD_RESET = "PASSWORD_RESET"


class Verification(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    type: VerificationType
    token: str

    user_id: uuid.UUID = Field(foreign_key="user.id")
    user: Optional["User"] = Relationship(back_populates="verifications")
