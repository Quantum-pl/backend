from typing import TYPE_CHECKING, Optional
from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime
import uuid

if TYPE_CHECKING:
    from .user import User


class Session(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    token: str
    refresh: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
    expire_at: datetime

    user_id: uuid.UUID = Field(foreign_key="user.id")
    user: Optional["User"] = Relationship(back_populates="sessions")
