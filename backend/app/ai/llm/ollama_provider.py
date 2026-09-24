import json
import re

from pydantic import ValidationError

from app.ai.llm.openai_provider import _load_prompt, _OpenAICompatibleBase, make_async_client
from app.core.config import settings

_FENCE = re.compile(r"^\s*```(?:json)?\s*|\s*```\s*$", re.IGNORECASE)


def _coerce_json(content: str) -> str:
    """Recover a JSON payload from a model reply. Ollama models often wrap output in
    markdown fences or add prose despite instructions, so strip fences and, failing
    that, grab the outermost {...} / [...] span."""
    text = content.strip()
    if text.startswith("```"):
        text = _FENCE.sub("", text).strip()
    try:
        json.loads(text)
        return text
    except json.JSONDecodeError:
        pass
    for open_ch, close_ch in (("{", "}"), ("[", "]")):
        start, end = text.find(open_ch), text.rfind(close_ch)
        if start != -1 and end > start:
            candidate = text[start : end + 1]
            try:
                json.loads(candidate)
                return candidate
            except json.JSONDecodeError:
                continue
    return text


class OllamaCloudProvider(_OpenAICompatibleBase):
    """Ollama Cloud via its OpenAI-compatible endpoint (default https://ollama.com/v1).
    Used when LLM_PROVIDER=ollama and OLLAMA_API_KEY is configured.

    Unlike OpenAI, Ollama does not reliably honour strict json_schema structured
    output, so instead of the `.parse` helper we use JSON-object mode with the schema
    injected into the prompt, then validate defensively (fence-stripping + one retry)."""

    name = "ollama"

    def __init__(
        self,
        *,
        model: str | None = None,
        api_key: str | None = None,
        base_url: str | None = None,
    ) -> None:
        super().__init__(
            model=model or settings.ollama_model,
            api_key=api_key or settings.ollama_api_key,
            base_url=base_url or settings.ollama_base_url,
        )

    async def extract(self, *, kind, transcript_text, response_model, hint=None):  # type: ignore[no-untyped-def]
        schema = json.dumps(response_model.model_json_schema())
        system = (
            f"{_load_prompt(kind)}\n\n"
            "Respond with ONLY a single JSON value that conforms to this JSON Schema. "
            "Do not include markdown code fences, comments, or any explanatory text.\n"
            f"JSON Schema:\n{schema}"
        )
        client = make_async_client(self._api_key, self._base_url)

        last_error: Exception | None = None
        for _attempt in range(2):
            completion = await client.chat.completions.create(
                model=self._model,
                messages=[
                    {"role": "system", "content": system},
                    {"role": "user", "content": transcript_text},
                ],
                response_format={"type": "json_object"},
                temperature=0,
            )
            content = completion.choices[0].message.content or ""
            try:
                return response_model.model_validate_json(_coerce_json(content))
            except ValidationError as exc:
                last_error = exc
                system += (
                    "\n\nYour previous reply did not match the schema. "
                    "Return ONLY the valid JSON value, nothing else."
                )

        raise RuntimeError(
            f"Ollama model {self._model!r} did not return schema-valid JSON for "
            f"'{kind}' after 2 attempts: {last_error}"
        )
