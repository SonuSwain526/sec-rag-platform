"""
Core Configuration Module for sec-rag.

This module defines the global configuration settings for the backend application
using Pydantic v2 Settings. It loads environment variables, sets defaults,
and validates connection URIs and credentials.
"""

from typing import List, Optional
from pydantic import AnyHttpUrl, BeforeValidator, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Application settings loaded from environment variables and dotenv configurations.
    """
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore"
    )

    PROJECT_NAME: str = "sec-rag"
    API_V1_STR: str = "/api/v1"
    
    # Security Settings
    JWT_SECRET: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 115200  # Default to 8 days

    # Database Settings
    DATABASE_URL: str

    # Vector Database Settings
    QDRANT_URL: str
    QDRANT_API_KEY: Optional[str] = None

    # External LLM & Embedding APIs
    GROQ_API_KEY: Optional[str] = None
    OPENAI_API_KEY: Optional[str] = None
    HF_TOKEN: Optional[str] = None

    # App CORS Origins
    BACKEND_CORS_ORIGINS: List[str] = ["http://localhost:5173", "http://127.0.0.1:5173"]

    @field_validator("DATABASE_URL")
    @classmethod
    def validate_database_url(cls, v: str) -> str:
        """
        Ensures the database connection URL is formatted correctly.
        """
        # TODO: Add specific checks for asyncpg or postgresql dialects
        if not v.startswith("postgresql://") and not v.startswith("postgresql+asyncpg://"):
            raise ValueError("DATABASE_URL must start with 'postgresql://' or 'postgresql+asyncpg://'")
        return v

    @field_validator("QDRANT_URL")
    @classmethod
    def validate_qdrant_url(cls, v: str) -> str:
        """
        Validates the Qdrant connection URL.
        """
        # TODO: Implement strict host/port validation
        if not v.startswith("http://") and not v.startswith("https://") and not v.startswith("localhost:"):
            raise ValueError("QDRANT_URL must be a valid http/https URL or local address")
        return v


# Instantiate global settings object
# TODO: Implement caching/singleton pattern if settings need lazy loading
settings = Settings()
