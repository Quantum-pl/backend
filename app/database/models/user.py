from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import Mapped
from app.database.models import Base

class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = Column(Integer, primary_key=True)
    username: Mapped[str] = Column(String(50), unique=True, nullable=False)

    def __repr__(self):
        return f"<User(id={self.id}, username={self.username})>"