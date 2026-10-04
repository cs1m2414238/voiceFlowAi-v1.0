import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[2]


class Settings:
    """Application configuration loaded from environment variables."""

    def __init__(self) -> None:
        self.APP_NAME: str = os.getenv("APP_NAME", "VoiceFlow AI")
        self.APP_ENV: str = os.getenv("APP_ENV", "development")
        self.DEBUG: bool = os.getenv("DEBUG", "false").lower() in ("true", "1", "yes")
        self.HOST: str = os.getenv("HOST", "0.0.0.0")
        self.PORT: int = int(os.getenv("PORT", "8000"))

        # LLM / Ollama settings
        self.OLLAMA_BASE_URL: str = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
        self.OLLAMA_MODEL: str = os.getenv("OLLAMA_MODEL", "llama3.2:3b")
        self.LLM_TEMPERATURE: float = float(os.getenv("LLM_TEMPERATURE", "0.0"))

        # RAG / ChromaDB settings
        self.CHROMA_PERSIST_DIR: str = os.getenv(
            "CHROMA_PERSIST_DIR", str(BASE_DIR / "chroma_test_db")
        )
        self.EMBEDDING_MODEL: str = os.getenv(
            "EMBEDDING_MODEL", "sentence-transformers/all-MiniLM-L6-v2"
        )
        self.DEFAULT_FAQ_PDF: str = os.getenv(
            "DEFAULT_FAQ_PDF", str(BASE_DIR / "company_faq.pdf")
        )

        # Java Backend integration settings
        self.JAVA_BACKEND_URL: str = os.getenv("JAVA_BACKEND_URL", "http://localhost:8080")
        self.JAVA_BACKEND_TIMEOUT: float = float(os.getenv("JAVA_BACKEND_TIMEOUT", "3.0"))
        self.JAVA_SYNC_ENABLED: bool = os.getenv(
            "JAVA_SYNC_ENABLED", "false"
        ).lower() in ("true", "1", "yes")

        # Security
        self.API_KEY: str = os.getenv("API_KEY", "")

        # Speech settings
        self.MAX_AUDIO_SIZE_MB: int = int(os.getenv("MAX_AUDIO_SIZE_MB", "25"))
        self.DEFAULT_TTS_VOICE: str = os.getenv("DEFAULT_TTS_VOICE", "Rachel")
        self.DEFAULT_STT_LANGUAGE: str = os.getenv("DEFAULT_STT_LANGUAGE", "en")


settings = Settings()


def get_settings() -> Settings:
    return settings
