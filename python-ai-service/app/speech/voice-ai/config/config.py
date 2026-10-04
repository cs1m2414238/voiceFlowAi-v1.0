import os
from typing import Optional
from pydantic_settings import BaseSettings, SettingsConfigDict


class VoiceSettings(BaseSettings):
    """Configuration settings for Voice AI STT and TTS services."""
    APP_NAME: str = "Voice AI Module"
    ENVIRONMENT: str = "development"
    DEBUG: bool = True

    # Voice STT Configuration
    # Options: "faster-whisper", "mock"
    STT_PROVIDER: str = "faster-whisper"

    # Voice TTS Configuration
    # Options: "elevenlabs", "edge-tts", "gtts", "mock"
    TTS_PROVIDER: str = "edge-tts"
    ELEVENLABS_API_KEY: Optional[str] = None

    # Audio Directory Storage
    AUDIO_DIR: str = "./audio_storage"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )


settings = VoiceSettings()
