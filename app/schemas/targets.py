from pydantic import BaseModel, Field, HttpUrl, ConfigDict
from typing import Optional
from datetime import datetime


class TargetBase(BaseModel):
    url: HttpUrl
    name: str
    check_interval: int = Field(1, gt=0)


class Target(TargetBase):
    id: int
    status: Optional[str] = Field('PENDING')
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: Optional[datetime] = Field(default_factory=datetime.now)

    model_config = ConfigDict(from_attributes=True)


class TargetCreate(TargetBase):
    pass


class TargetResponse(TargetBase):
    id: int
    status: str