from app.ai.engines.base import CodingEngine
from app.ai.engines.mock import MockCodingEngine
from app.core.config import settings


def get_coding_engine() -> CodingEngine:
    """Return the configured coding engine (CODING_ENGINE: mock | claude)."""
    if settings.coding_engine == "claude":
        from app.ai.engines.claude_agent import ClaudeAgentEngine

        return ClaudeAgentEngine()
    return MockCodingEngine()
