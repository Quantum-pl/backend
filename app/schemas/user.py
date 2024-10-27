from pydantic import BaseModel
from uuid import UUID
from datetime import datetime
from typing import Optional


class UserBase(BaseModel):
    first_name: str
    last_name: str

class UserRead(UserBase):
    id: UUID
    avatar: Optional[str]
    created_at: datetime

class UserUpdate(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[str] = None
    avatar: Optional[str] = None
    phone: Optional[str] = None