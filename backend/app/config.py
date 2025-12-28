from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    # Database
    DATABASE_URL: str = "postgresql://spendly:spendly@localhost:5432/spendly"

    # AI APIs
    ANTHROPIC_API_KEY: str | None = None
    OPENAI_API_KEY: str | None = None

    # App
    APP_NAME: str = "Spendly"
    DEBUG: bool = True

    # Security
    JWT_SECRET_KEY: str = "change-this-in-production-use-long-random-string"
    JWT_ALGORITHM: str = "HS256"
    JWT_EXPIRE_MINUTES: int = 30

    class Config:
        env_file = "../.env"


@lru_cache()
def get_settings():
    return Settings()