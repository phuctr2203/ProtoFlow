from pathlib import Path

from app.core.config import settings

_PROMPTS = Path(__file__).resolve().parent.parent / "prompts" / "meeting_intelligence"


def _load_prompt(kind: str) -> str:
    path = _PROMPTS / f"{kind}.txt"
    if path.exists():
        return path.read_text(encoding="utf-8")
    return f"Extract the {kind} from the meeting transcript as structured data."


def make_async_client(api_key: str | None, base_url: str | None):  # type: ignore[no-untyped-def]
    """Build an AsyncOpenAI client, wrapped for LangSmith tracing when enabled so
    every model call is captured as a nested run inside the LangGraph trace."""
    from openai import AsyncOpenAI

    client = AsyncOpenAI(api_key=api_key, base_url=base_url)
    if settings.langsmith_tracing:
        try:
            from langsmith.wrappers import wrap_openai

            client = wrap_openai(client)
        except Exception:  # pragma: no cover - tracing must never break inference
            pass
    return client


class _OpenAICompatibleBase:
    """Shared implementation for any OpenAI-compatible chat/completions API.
    Concrete providers supply their own name, model, key and base URL."""

    name = "openai-compatible"

    def __init__(self, *, model: str, api_key: str | None, base_url: str | None) -> None:
        self._model = model
        self._api_key = api_key
        self._base_url = base_url

    async def extract(self, *, kind, transcript_text, response_model, hint=None):  # type: ignore[no-untyped-def]
        client = make_async_client(self._api_key, self._base_url)
        completion = await client.beta.chat.completions.parse(
            model=self._model,
            messages=[
                {"role": "system", "content": _load_prompt(kind)},
                {"role": "user", "content": transcript_text},
            ],
            response_format=response_model,
        )
        parsed = completion.choices[0].message.parsed
        return parsed if parsed is not None else response_model()


class OpenAICompatibleProvider(_OpenAICompatibleBase):
    """Real provider for any OpenAI-compatible API (OpenAI, Azure AI Foundry, local).
    Used when LLM_PROVIDER=openai and a key is configured."""

    name = "openai"

    def __init__(
        self,
        *,
        model: str | None = None,
        api_key: str | None = None,
        base_url: str | None = None,
    ) -> None:
        super().__init__(
            model=model or settings.openai_model,
            api_key=api_key or settings.openai_api_key,
            base_url=base_url or settings.openai_base_url,
        )
