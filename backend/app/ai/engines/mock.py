from pathlib import Path

from app.ai.schemas.development import CodingResult, DevelopmentPlan, RepositoryInspection

_BRANCH = "protoflow/generated-mvp"


class MockCodingEngine:
    """Deterministic coding engine for offline dev and tests. It materializes a small, honest
    scaffold in the workspace from the development plan instead of calling a real coding agent."""

    name = "mock"

    async def implement(
        self,
        *,
        workspace: str,
        plan: DevelopmentPlan,
        inspection: RepositoryInspection,
        mvp_text: str,
    ) -> CodingResult:
        root = Path(workspace)
        root.mkdir(parents=True, exist_ok=True)

        files_changed: list[str] = []
        tests_written: list[str] = []

        plan_lines = "\n".join(
            f"- [{t.order}] {t.id} ({t.component}): {t.title}" for t in plan.tasks
        )
        readme = root / "GENERATED_PLAN.md"
        readme.write_text(
            "# Generated MVP scaffold\n\n"
            "This scaffold was produced by the mock coding engine.\n\n"
            f"## Tasks\n{plan_lines}\n",
            encoding="utf-8",
        )
        files_changed.append("GENERATED_PLAN.md")

        for task in plan.tasks:
            stub = root / f"{task.id.lower().replace('-', '_')}.md"
            stub.write_text(f"# {task.id}: {task.title}\n\n{task.description}\n", encoding="utf-8")
            files_changed.append(stub.name)

        test_file = root / "test_smoke.md"
        test_file.write_text(
            "# Smoke test placeholder\n\nGenerated MVP builds.\n", encoding="utf-8"
        )
        tests_written.append(test_file.name)

        return CodingResult(
            summary=f"Scaffolded {len(plan.tasks)} tasks into the workspace (mock engine).",
            files_changed=sorted(files_changed),
            tests_written=tests_written,
            branch=_BRANCH,
        )
