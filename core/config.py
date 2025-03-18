import os
from typing import List

from dotenv import load_dotenv
from pydantic import model_validator
from pydantic_settings import BaseSettings

load_dotenv()


class Settings(BaseSettings):
    """Application settings"""

    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "Geolocation API"

    DB_ENGINE: str = os.getenv("DB_ENGINE", "postgresql")
    DB_NAME: str = os.getenv("DB_NAME", "geolocation_db")
    DB_USER: str = os.getenv("DB_USER", "postgres")
    DB_PASSWORD: str = os.getenv("DB_PASSWORD", "")
    DB_HOST: str = os.getenv("DB_HOST", "localhost")
    DB_PORT: str = os.getenv("DB_PORT", "5432")

    @property
    def DATABASE_URL(self) -> str:
        return f"{self.DB_ENGINE}://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    IPSTACK_API_KEY: str = os.getenv("IPSTACK_API_KEY", "")

    DEBUG: bool = os.getenv("DEBUG", "False").lower() == "true"

    TIME_ZONE: str = "UTC"
    LANGUAGE_CODE: str = "en-us"

    # This runs after model creation
    @model_validator(mode="after")
    def set_allowed_hosts(self):
        # Get ALLOWED_HOSTS directly from environment
        allowed_hosts_str = os.getenv("ALLOWED_HOSTS", "localhost,127.0.0.1")
        self._allowed_hosts = [
            host.strip() for host in allowed_hosts_str.split(",") if host.strip()
        ]
        return self

    @property
    def ALLOWED_HOSTS(self) -> List[str]:
        if hasattr(self, "_allowed_hosts"):
            return self._allowed_hosts
        return ["localhost", "127.0.0.1"]

    model_config = {
        "case_sensitive": True,
        "env_file": ".env",
        "extra": "ignore",
    }


def get_settings() -> Settings:
    class OverrideSettings(Settings):
        model_config = {
            "env_file": ".env.override",
            "env_file_encoding": "utf-8",
            "extra": "ignore",
        }

    if os.path.exists(".env.override"):
        return OverrideSettings()
    else:
        return Settings()
