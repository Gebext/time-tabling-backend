"""
Application configuration using Pydantic Settings.
All environment variables and app-wide settings are managed here.
"""

import os
from functools import lru_cache

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Global application settings loaded from environment / .env file."""

    # ── App ──────────────────────────────────────────────
    APP_NAME: str = "GA-GWO Timetabling API"
    APP_VERSION: str = "1.0.0"
    APP_DESCRIPTION: str = (
        "Sistem penjadwalan sekolah otomatis menggunakan "
        "Hybrid Genetic Algorithm & Grey Wolf Optimizer"
    )
    DEBUG: bool = True

    # ── Server ───────────────────────────────────────────
    HOST: str = "0.0.0.0"
    PORT: int = 8000

    # ── CORS ─────────────────────────────────────────────
    CORS_ORIGINS: list[str] = ["*"]

    # ── Data ─────────────────────────────────────────────
    DATA_DIR: str = os.path.join(
        os.path.dirname(os.path.dirname(__file__)), "data", "csv"
    )

    # ── Algorithm defaults ───────────────────────────────
    DEFAULT_POPULATION_SIZE: int = 50
    DEFAULT_MAX_ITERATIONS: int = 1500
    DEFAULT_TOURNAMENT_SIZE: int = 15

    model_config = {
        "env_file": os.path.join(
            os.path.dirname(os.path.dirname(__file__)), ".env"
        ),
        "env_file_encoding": "utf-8",
        "extra": "ignore",
    }


@lru_cache()
def get_settings() -> Settings:
    """Cached singleton for application settings."""
    return Settings()
