from functools import lru_cache
from pathlib import Path
from pydantic import BaseSettings, Field


class Settings(BaseSettings):
    DB_URL: str = Field("sqlite://../local.db")
    BACKUP_FOLDER: Path = Field(Path(__file__).parent / "Backup")


@lru_cache
def get_settings() -> Settings:
    return Settings()
