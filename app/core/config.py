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

    # LLM / Brain settings
    brain_model: str = "qwen2.5:3b"
    brain_temperature: float = 0.2
    brain_num_ctx: int = 4096

    # Voice TTS settings (High energy expressive female voice defaults)
    tts_voice: str = "en-US-AvaNeural"
    tts_rate: str = "+8%"
    tts_pitch: str = "+3Hz"

    # Voice STT Listening settings
    stt_pause_threshold: float = 5.0  # Waits for 5 seconds of silence after speaking before finalizing
    stt_timeout: float = 10.0
    stt_phrase_time_limit: float = 25.0

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


settings = Settings()