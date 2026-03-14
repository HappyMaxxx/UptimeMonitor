import os
from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class Settings(BaseSettings):
    redis_url: str
    celery_broker_url: str
    celery_result_backend: str
    
    database_url: str

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore"
    )

@lru_cache()
def get_settings() -> Settings:
    return Settings()