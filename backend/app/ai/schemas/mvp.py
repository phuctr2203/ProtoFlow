import enum

from pydantic import BaseModel, Field


class Scope(enum.StrEnum):
    MUST_HAVE = "MUST_HAVE"
    SHOULD_HAVE = "SHOULD_HAVE"
    NICE_TO_HAVE = "NICE_TO_HAVE"
    OUT_OF_SCOPE = "OUT_OF_SCOPE"


class Feature(BaseModel):
    name: str
    description: str = ""
    scope: Scope = Scope.MUST_HAVE


class MVPSpecification(BaseModel):
    objective: str = ""
    target_users: list[str] = Field(default_factory=list)
    goals: list[str] = Field(default_factory=list)
    features: list[Feature] = Field(default_factory=list)
    user_journeys: list[str] = Field(default_factory=list)
    acceptance_criteria: list[str] = Field(default_factory=list)
    out_of_scope: list[str] = Field(default_factory=list)
    assumptions: list[str] = Field(default_factory=list)
    open_questions: list[str] = Field(default_factory=list)
    demo_scenario: str = ""


# ---- per-agent (node) response models ----


class MVPCore(BaseModel):
    objective: str = ""
    target_users: list[str] = Field(default_factory=list)
    goals: list[str] = Field(default_factory=list)


class FeatureList(BaseModel):
    features: list[Feature] = Field(default_factory=list)


class UXPlan(BaseModel):
    user_journeys: list[str] = Field(default_factory=list)
    acceptance_criteria: list[str] = Field(default_factory=list)
    demo_scenario: str = ""


class Critique(BaseModel):
    out_of_scope: list[str] = Field(default_factory=list)
    assumptions: list[str] = Field(default_factory=list)
    open_questions: list[str] = Field(default_factory=list)
    notes: list[str] = Field(default_factory=list)
