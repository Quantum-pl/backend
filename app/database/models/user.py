import uuid
from datetime import datetime
from typing import List, Optional, TYPE_CHECKING

from sqlmodel import SQLModel, Field, Relationship

if TYPE_CHECKING:
    from .order import Order
    from .product import Product
    from .session import Session
    from .verify import Verification


class User(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    avatar: Optional[str]
    email: str = Field(index=True, unique=True)
    phone: Optional[str] = Field(unique=True)
    password: str
    first_name: str
    last_name: str
    is_email_verified: bool = Field(default=False)
    flags: int = Field(default=0)
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: Optional[datetime] = Field(default=None)

    sessions: List["Session"] = Relationship(back_populates="user")
    products: List["Product"] = Relationship(back_populates="user")
    orders: List["Order"] = Relationship(back_populates="user")
    verifications: List["Verification"] = Relationship(back_populates="user")
