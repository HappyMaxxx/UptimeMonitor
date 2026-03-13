from sqlalchemy import Column, Integer, String, Boolean, Enum, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base
from app.models.base import TimestampMixin


class Target(Base, TimestampMixin):
    __tablename__ = "targets"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    url = Column(String, nullable=False)
    check_interval = Column(Integer, nullable=False, default=1)  # in minutes
    status = Column(String, nullable=False, default='PENDING')  # PENDING,
    # UP, DOWN, CHECKING
