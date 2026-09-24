from app.ai.llm.registry import get_dev_llm_provider, get_llm_provider
from app.core.config import settings


def test_dev_team_inherits_shared_config(monkeypatch):
    """With no DEV_* overrides, the dev team resolves to the shared provider/model."""
    monkeypatch.setattr(settings, "llm_provider", "ollama")
    monkeypatch.setattr(settings, "ollama_model", "shared-model")
    monkeypatch.setattr(settings, "dev_llm_provider", None)
    monkeypatch.setattr(settings, "dev_ollama_model", None)

    product = get_llm_provider()
    dev = get_dev_llm_provider()

    assert product.name == "ollama"
    assert dev.name == "ollama"
    assert dev._model == "shared-model"


def test_dev_team_overrides_provider_and_model(monkeypatch):
    """DEV_* overrides let the dev team diverge from the product team."""
    monkeypatch.setattr(settings, "llm_provider", "mock")
    monkeypatch.setattr(settings, "dev_llm_provider", "ollama")
    monkeypatch.setattr(settings, "dev_ollama_model", "dev-coder-model")
    monkeypatch.setattr(settings, "dev_ollama_api_key", "dev-key")

    product = get_llm_provider()
    dev = get_dev_llm_provider()

    assert product.name == "mock"
    assert dev.name == "ollama"
    assert dev._model == "dev-coder-model"
    assert dev._api_key == "dev-key"
