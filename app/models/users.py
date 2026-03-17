from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import relationship, Mapped
from typing import List

from app.database import Base
from app.models.base import TimestampMixin
from app.models.targets import Target

class User(Base, TimestampMixin):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True, nullable=False)
    email = Column(String(255), unique=True, index=True, nullable=False)
    is_active = Column(Boolean, default=True)
    hashed_password = Column(String(255), nullable=False)

    targets: Mapped[List["Target"]] = relationship("Target", back_populates="owner",
                                                   cascade="all, delete-orphan")
