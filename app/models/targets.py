from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship, Mapped, mapped_column
from typing import List

from app.database import Base
from app.models.base import TimestampMixin

class Target(Base, TimestampMixin):
    __tablename__ = "targets"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    url: Mapped[str]  = mapped_column(String, nullable=False)
    check_interval: Mapped[int]  = mapped_column(Integer, nullable=False, default=1)
    status: Mapped[str] = mapped_column(String, nullable=False, default='PENDING')

    history: Mapped[List['TargetHistory']] = relationship(back_populates='tar', cascade="all, delete-orphan")


class TargetHistory(Base, TimestampMixin):
    __tablename__ = "target_history"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    target_id: Mapped[int] = mapped_column(ForeignKey("targets.id", ondelete="CASCADE"), nullable=False)
    
    status: Mapped[str] = mapped_column(String, nullable=False, default='PENDING')

    tar: Mapped['Target'] = relationship(back_populates='history')