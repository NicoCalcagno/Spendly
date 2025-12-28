from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    # Database
    DATABASE_URL: str = "postgresql://spendly:spendly@localhost:5432/spendly"

    # Claude API
    ANTHROPIC_API_KEY: str | None = None

    # App
    APP_NAME: str = "Spendly"
    DEBUG: bool = True

    class Config:
        env_file = ".env"


@lru_cache()
def get_settings():
    return Settings()