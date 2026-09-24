import enum

from pydantic import BaseModel, Field


class CapabilityStatus(enum.StrEnum):
    IMPLEMENTED = "IMPLEMENTED"
    SIMULATED = "SIMULATED"
    NOT_IMPLEMENTED = "NOT_IMPLEMENTED"


class DemoStep(BaseModel):
    order: int = 0
    action: str
    expected: str = ""


class Capability(BaseModel):
    name: str
    status: CapabilityStatus
    note: str = ""


class DemoNarrative(BaseModel):
    """LLM-authored part of the demo (objective, script, synthetic data). Capability labels are
    NOT set here — they are derived from QA evidence so the demo never overclaims (FR-19)."""

    objective: str = ""
    script: list[DemoStep] = Field(default_factory=list)
    synthetic_data: list[str] = Field(default_factory=list)
    known_limitations: list[str] = Field(default_factory=list)
    next_steps: list[str] = Field(default_factory=list)


class DemoPackage(DemoNarrative):
    """Full demo package: the narrative plus honest, evidence-derived capability labels."""

    capabilities: list[Capability] = Field(default_factory=list)
