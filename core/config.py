import os
from typing import List
from pydantic import model_validator
from pydantic_settings import BaseSettings
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


class Settings(BaseSettings):
    """Application settings"""

    # API Settings
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "Geolocation API"

    # Database settings
    DB_ENGINE: str = os.getenv("DB_ENGINE", "postgresql")
    DB_NAME: str = os.getenv("DB_NAME", "geolocation_db")
    DB_USER: str = os.getenv("DB_USER", "postgres")
    DB_PASSWORD: str = os.getenv("DB_PASSWORD", "")
    DB_HOST: str = os.getenv("DB_HOST", "localhost")
    DB_PORT: str = os.getenv("DB_PORT", "5432")

    # Construct the database URL
    @property
    def DATABASE_URL(self) -> str:
        return f"{self.DB_ENGINE}://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    # API Keys
    IPSTACK_API_KEY: str = os.getenv("IPSTACK_API_KEY", "")

    # Application settings
    DEBUG: bool = os.getenv("DEBUG", "False").lower() == "true"

    # Don't define ALLOWED_HOSTS here - we'll set it manually after validation
    # Application localization settings
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
        # Skip validation for environment variables not defined in the model
        "extra": "ignore",
    }


def get_settings() -> Settings:
    return Settings()
