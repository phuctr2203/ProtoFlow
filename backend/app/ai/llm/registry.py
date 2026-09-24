from dataclasses import dataclass

from app.ai.llm.base import LLMProvider
from app.ai.llm.mock import MockLLMProvider
from app.core.config import settings

# LLM teams. The product team (Epics 2-5: meeting intelligence, MVP, design) and the
# developer team (Epics 6-7: AI development, QA) resolve their providers independently,
# so the dev/QA agents can run on a different provider or model in future.
PRODUCT_TEAM = "product"
DEV_TEAM = "dev"


@dataclass(frozen=True)
class _LLMConfig:
    provider: str
    openai_api_key: str | None
    openai_base_url: str | None
    openai_model: str
    ollama_api_key: str | None
    ollama_base_url: str
    ollama_model: str


def _config_for(team: str) -> _LLMConfig:
    """Resolve the effective LLM config for a team. Dev-team overrides fall back to the
    shared (product) values when unset, so the dev team works with no extra config today."""
    s = settings
    if team == DEV_TEAM:
        return _LLMConfig(
            provider=s.dev_llm_provider or s.llm_provider,
            openai_api_key=s.dev_openai_api_key or s.openai_api_key,
            openai_base_url=s.dev_openai_base_url or s.openai_base_url,
            openai_model=s.dev_openai_model or s.openai_model,
            ollama_api_key=s.dev_ollama_api_key or s.ollama_api_key,
            ollama_base_url=s.dev_ollama_base_url or s.ollama_base_url,
            ollama_model=s.dev_ollama_model or s.ollama_model,
        )
    return _LLMConfig(
        provider=s.llm_provider,
        openai_api_key=s.openai_api_key,
        openai_base_url=s.openai_base_url,
        openai_model=s.openai_model,
        ollama_api_key=s.ollama_api_key,
        ollama_base_url=s.ollama_base_url,
        ollama_model=s.ollama_model,
    )


def get_llm_provider(team: str = PRODUCT_TEAM) -> LLMProvider:
    """Return the configured LLM provider for a team (default: the product team)."""
    cfg = _config_for(team)
    if cfg.provider == "openai":
        from app.ai.llm.openai_provider import OpenAICompatibleProvider

        return OpenAICompatibleProvider(
            model=cfg.openai_model,
            api_key=cfg.openai_api_key,
            base_url=cfg.openai_base_url,
        )
    if cfg.provider == "ollama":
        from app.ai.llm.ollama_provider import OllamaCloudProvider

        return OllamaCloudProvider(
            model=cfg.ollama_model,
            api_key=cfg.ollama_api_key,
            base_url=cfg.ollama_base_url,
        )
    return MockLLMProvider()


def get_dev_llm_provider() -> LLMProvider:
    """LLM provider for the developer team (Epics 6-7: AI development & QA)."""
    return get_llm_provider(DEV_TEAM)
