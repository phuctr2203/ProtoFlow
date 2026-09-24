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

    # Developer-team LLM (Epics 6-7: AI development & QA). Each override is optional and
    # inherits the shared value above when unset, so the dev/QA agents can later run on a
    # different provider or model without affecting the product team (Epics 2-5).
    dev_llm_provider: str | None = None
    dev_openai_api_key: str | None = None
    dev_openai_base_url: str | None = None
    dev_openai_model: str | None = None
    dev_ollama_api_key: str | None = None
    dev_ollama_base_url: str | None = None
    dev_ollama_model: str | None = None

    # Coding engine (Epic 6, Story 6.3) — "mock" scaffolds offline; "claude" wraps the Claude
    # Agent SDK (needs anthropic_api_key, or claude_code_oauth_token for solo use only).
    coding_engine: str = "mock"
    anthropic_api_key: str | None = None
    claude_code_oauth_token: str | None = None
    workspace_root: str = "/tmp/protoflow-workspaces"

    # Epic 6 infra — vector retrieval (Qdrant) and artifact/object storage (MinIO), used by
    # the generated document-Q&A MVP. Compose overrides the hosts with service names.
    qdrant_url: str = "http://localhost:6333"
    minio_endpoint: str = "localhost:9000"
    minio_access_key: str = "protoflow"
    minio_secret_key: str = "protoflow"
    minio_bucket: str = "protoflow-artifacts"
    minio_secure: bool = False

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
