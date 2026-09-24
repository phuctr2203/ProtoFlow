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
