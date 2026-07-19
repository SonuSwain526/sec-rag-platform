from functools import lru_cache
from typing import List
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict



class Settings(BaseSettings):
    """
    Centralized, typed application configuration.
    Values are loaded from environment variables / .env file.
    Pydantic validates types at startup — misconfiguration fails
    immediately instead of causing silent bugs later.
    """

    

    # App
    APP_NAME: str = "SEC Filings RAG"
    ENVIRONMENT: str = "development"  # development | production
    DEBUG: bool = True
    BACKEND_CORS_ORIGINS: List[str] = ["*"]  # dev only — restrict to real frontend domain in production

    # Database
    DATABASE_URL: str = "sqlite:///./sec_rag.db"

    # JWT Auth
    JWT_SECRET_KEY: str  # REQUIRED — no default on purpose. App must fail to start if missing.
    JWT_ALGORITHM: str = "HS256"
    JWT_EXPIRE_MINUTES: int = 60  # 1 hour — adjust deliberately, not by accident

    # Qdrant
    QDRANT_URL: str = "http://localhost:6333"
    QDRANT_API_KEY: str | None = None  # only needed if using Qdrant Cloud
    QDRANT_COLLECTION_NAME: str = "sec_filings"

    # Embedding model
    EMBEDDING_MODEL_NAME: str = "BAAI/bge-large-en-v1.5"
    EMBEDDING_DIMENSION: int = 1024

    # Reranker
    RERANKER_MODEL_NAME: str = "BAAI/bge-reranker-large"

    # LLM (Groq)
    GROQ_API_KEY: str
    GROQ_MODEL_NAME: str = "llama-3.3-70b-versatile"

    # SEC EDGAR
    SEC_EDGAR_USER_AGENT: str  # SEC requires a descriptive User-Agent header on every request

    model_config = SettingsConfigDict(
        env_file=Path(__file__).resolve().parent.parent.parent / ".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
    )

@lru_cache
def get_settings() -> Settings:
    """
    Cached settings instance — avoids re-parsing .env on every call.
    Use as a FastAPI dependency: `settings: Settings = Depends(get_settings)`
    """
    return Settings()