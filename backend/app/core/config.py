from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    app_env: str = "development"
    log_level: str = "INFO"
    api_v1_prefix: str = "/api/v1"

    database_url: str = "postgresql+asyncpg://protoflow:protoflow@localhost:5432/protoflow"
    redis_url: str = "redis://localhost:6379/0"

    cors_origins: list[str] = ["http://localhost:5173"]

    # LLM provider (Idea.MD §6.3) — "mock" runs offline with deterministic output.
    llm_provider: str = "mock"
    openai_api_key: str | None = None
    openai_base_url: str | None = None
    openai_model: str = "gpt-4o-mini"

    # Confidence thresholds (Idea.MD §54, NFR6) — configurable, not hardcoded.
    confidence_high: float = 0.90
    confidence_needs_review: float = 0.70


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
