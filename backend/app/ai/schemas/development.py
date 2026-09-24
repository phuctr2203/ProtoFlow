from pydantic import BaseModel, Field


class DevelopmentTask(BaseModel):
    """One unit of implementation work in the ordered development plan (Idea.MD §28, §30)."""

    id: str
    title: str
    description: str = ""
    component: str = "backend"  # frontend | backend | ai | infra
    depends_on: list[str] = Field(default_factory=list)  # ids of prerequisite tasks
    order: int = 0


class DevelopmentPlan(BaseModel):
    """Ordered task breakdown produced by the Development Manager (FR-14)."""

    tasks: list[DevelopmentTask] = Field(default_factory=list)


class RepositoryInspection(BaseModel):
    """Structured facts about an existing repository, gathered before any code is written
    so the coding agents follow existing conventions instead of rewriting (Idea.MD §31 Rule 1)."""

    file_count: int = 0
    languages: dict[str, int] = Field(default_factory=dict)  # extension -> file count
    frameworks: list[str] = Field(default_factory=list)
    entry_points: list[str] = Field(default_factory=list)  # marker files (pyproject.toml, etc.)
    top_level: list[str] = Field(default_factory=list)  # top-level entries in the repo
    notes: list[str] = Field(default_factory=list)
