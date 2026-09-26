"""Claude Agent SDK coding engine (Story 6.0 decision). Enabled with CODING_ENGINE=claude.

Requires the `claude-agent-sdk` package and the Claude Code CLI available in the image, plus auth
via ANTHROPIC_API_KEY (the compliant path for a multi-tenant backend) or, for solo/self-host only,
CLAUDE_CODE_OAUTH_TOKEN. The import is lazy so the mock path never needs these installed.

NOTE: this path runs a real agent against the workspace and cannot be exercised offline; it is gated
and covered by Story 6.5 (isolated execution) before being used against untrusted output."""

import os
from pathlib import Path

from app.ai.schemas.development import CodingResult, DevelopmentPlan, RepositoryInspection
from app.core.config import settings

_BRANCH = "protoflow/generated-mvp"


def _build_prompt(plan: DevelopmentPlan, inspection: RepositoryInspection, mvp_text: str) -> str:
    tasks = "\n".join(
        f"{t.order}. [{t.component}] {t.id} — {t.title}: {t.description}" for t in plan.tasks
    )
    return (
        "You are ProtoFlow's coding agent. Implement the MVP in the current workspace, following "
        "existing conventions. Write accompanying tests. Do not commit or push.\n\n"
        f"Repository facts: {inspection.model_dump_json()}\n\n"
        f"MVP specification (JSON):\n{mvp_text}\n\n"
        f"Ordered development tasks:\n{tasks}\n"
    )


class ClaudeAgentEngine:
    """Wraps the Claude Agent SDK. Lazy-imported so it is only required when selected."""

    name = "claude"

    def _ensure_auth(self) -> None:
        if settings.anthropic_api_key:
            os.environ.setdefault("ANTHROPIC_API_KEY", settings.anthropic_api_key)
        elif settings.claude_code_oauth_token:
            os.environ.setdefault("CLAUDE_CODE_OAUTH_TOKEN", settings.claude_code_oauth_token)
        else:
            raise RuntimeError(
                "ClaudeAgentEngine needs ANTHROPIC_API_KEY (recommended) or "
                "CLAUDE_CODE_OAUTH_TOKEN (solo use only) to be set."
            )

    async def implement(
        self,
        *,
        workspace: str,
        plan: DevelopmentPlan,
        inspection: RepositoryInspection,
        mvp_text: str,
    ) -> CodingResult:
        self._ensure_auth()
        try:
            from claude_agent_sdk import ClaudeAgentOptions, query
        except ImportError as exc:  # pragma: no cover - optional heavy dependency
            raise RuntimeError(
                "claude-agent-sdk is not installed. Install it and the Claude Code CLI to use "
                "CODING_ENGINE=claude."
            ) from exc

        root = Path(workspace)
        root.mkdir(parents=True, exist_ok=True)
        before = {p for p in root.rglob("*") if p.is_file()}

        prompt = _build_prompt(plan, inspection, mvp_text)
        options = ClaudeAgentOptions(cwd=str(root), permission_mode="acceptEdits")
        messages: list[str] = []
        async for message in query(prompt=prompt, options=options):  # pragma: no cover - live only
            messages.append(str(message))

        after = {p for p in root.rglob("*") if p.is_file()}
        changed = sorted(str(p.relative_to(root)) for p in after - before)
        return CodingResult(
            summary=messages[-1] if messages else "Claude Agent SDK run complete.",
            files_changed=changed,
            tests_written=[f for f in changed if "test" in f.lower()],
            branch=_BRANCH,
        )
