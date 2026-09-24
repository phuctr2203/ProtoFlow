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

    # LLM provider (Idea.MD §6.3) — switchable via LLM_PROVIDER:
    #   "mock"   — offline deterministic output (default)
    #   "openai" — any OpenAI-compatible API (OpenAI, Azure AI Foundry, local)
    #   "ollama" — Ollama Cloud via its OpenAI-compatible endpoint
    llm_provider: str = "mock"

    openai_api_key: str | None = None
    openai_base_url: str | None = None
    openai_model: str = "gpt-4o-mini"

    ollama_api_key: str | None = None
    ollama_base_url: str = "https://ollama.com/v1"
    ollama_model: str = "gpt-oss:120b"

    # LangSmith tracing — monitors the LangGraph chains and LLM calls when enabled.
    langsmith_tracing: bool = False
    langsmith_api_key: str | None = None
    langsmith_project: str = "protoflow"
    langsmith_endpoint: str = "https://api.smith.langchain.com"

    # Confidence thresholds (Idea.MD §54, NFR6) — configurable, not hardcoded.
    confidence_high: float = 0.90
    confidence_needs_review: float = 0.70


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
