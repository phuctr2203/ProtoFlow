from typing import Protocol

from app.ai.schemas.development import CodingResult, DevelopmentPlan, RepositoryInspection


class CodingEngine(Protocol):
    """Config-driven code-generation layer (Story 6.0 decision). Callers depend on this, not on
    a concrete engine, so the Claude Agent SDK can be swapped for an OSS engine later (§31)."""

    name: str

    async def implement(
        self,
        *,
        workspace: str,
        plan: DevelopmentPlan,
        inspection: RepositoryInspection,
        mvp_text: str,
    ) -> CodingResult: ...
