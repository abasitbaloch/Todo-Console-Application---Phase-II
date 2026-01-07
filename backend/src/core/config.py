"""Application configuration from environment variables."""

import os
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import List


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    # --- Database ---
    # Default to /tmp/todo.db for Hugging Face write permissions
    DATABASE_URL: str = "sqlite:////tmp/todo.db"

    # --- JWT Configuration ---
    JWT_SECRET: str = "super-secret-key-change-this-in-production"
    JWT_ALGORITHM: str = "HS256"
    JWT_EXPIRATION_HOURS: int = 24

    # --- CORS Configuration ---
    # Default to allowing everything if not set, or your Vercel URL
    CORS_ORIGINS: str = "*"

    # --- Environment ---
    ENVIRONMENT: str = "development"

    @property
    def cors_origins_list(self) -> List[str]:
        """Parse CORS_ORIGINS into a list."""
        if self.CORS_ORIGINS == "*":
            return ["*"]
        return [origin.strip() for origin in self.CORS_ORIGINS.split(",")]

    # Use the newer Pydantic v2 ConfigDict style
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore" # Prevents crashing if extra variables are present
    )


settings = Settings()