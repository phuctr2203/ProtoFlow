from app.ai.llm.base import LLMProvider
from app.ai.llm.mock import MockLLMProvider
from app.core.config import settings


def get_llm_provider() -> LLMProvider:
    if settings.llm_provider == "openai":
        from app.ai.llm.openai_provider import OpenAICompatibleProvider

        return OpenAICompatibleProvider()
    return MockLLMProvider()
