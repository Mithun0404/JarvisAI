"""
Application configuration.

Loads configuration values from environment variables using
Pydantic Settings.
"""

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Global application settings.
    """

    app_name: str = "JARVIS"
    version: str = "0.1.0"
    author: str = "Mithun"

    environment: str = "development"

    log_level: str = "INFO"

    debug: bool = True

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


settings = Settings()