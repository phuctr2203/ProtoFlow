from pathlib import Path

from app.core.config import settings

_PROMPTS = Path(__file__).resolve().parent.parent / "prompts" / "meeting_intelligence"


def _load_prompt(kind: str) -> str:
    path = _PROMPTS / f"{kind}.txt"
    if path.exists():
        return path.read_text(encoding="utf-8")
    return f"Extract the {kind} from the meeting transcript as structured data."


class OpenAICompatibleProvider:
    """Real provider for any OpenAI-compatible API (OpenAI, Azure AI Foundry, local).
    Used when LLM_PROVIDER=openai and a key is configured."""

    name = "openai"

    def __init__(self) -> None:
        self._model = settings.openai_model
        self._api_key = settings.openai_api_key
        self._base_url = settings.openai_base_url

    async def extract(self, *, kind, transcript_text, response_model, hint=None):  # type: ignore[no-untyped-def]
        from openai import AsyncOpenAI

        client = AsyncOpenAI(api_key=self._api_key, base_url=self._base_url)
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
