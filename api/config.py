from functools import lru_cache
from pydantic import BaseSettings

class Settings(BaseSettings):
    MONGO_URI: str
    REDIS_URI: str
    API_KEY: str

    class Config:
        env_file = ".env"

@lru_cache()
def get_settings():
    return Settings()