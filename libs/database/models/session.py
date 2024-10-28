import uuid
from datetime import datetime
from typing import TYPE_CHECKING, Optional

from sqlmodel import SQLModel, Field, Relationship

if TYPE_CHECKING:
    from .user import User


class Session(SQLModel, table=True):
    __tablename__ = 'sessions'

    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: uuid.UUID = Field(foreign_key="users.id")

    access_token: str
    refresh_token: str

    created_at: datetime = Field(default_factory=datetime.now)
    expire_at: datetime

    user: Optional["User"] = Relationship(back_populates="sessions")
