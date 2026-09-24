from typing import Protocol, TypeVar

from pydantic import BaseModel

T = TypeVar("T", bound=BaseModel)


class LLMProvider(Protocol):
    """Config-driven LLM access layer (Idea.MD §6.3). Callers depend on this, not
    on a concrete provider or framework, so the backing model can be swapped freely."""

    name: str

    async def extract(
        self,
        *,
        kind: str,
        transcript_text: str,
        response_model: type[T],
        hint: str | None = None,
    ) -> T: ...
