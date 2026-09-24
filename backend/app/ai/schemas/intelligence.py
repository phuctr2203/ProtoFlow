import enum

from pydantic import BaseModel, Field


class RequirementType(enum.StrEnum):
    FUNCTIONAL = "functional"
    NON_FUNCTIONAL = "non_functional"


class Priority(enum.StrEnum):
    HIGH = "HIGH"
    MEDIUM = "MEDIUM"
    LOW = "LOW"


class Extraction(enum.StrEnum):
    EXPLICIT = "EXPLICIT"
    INFERRED = "INFERRED"


class RequirementStatus(enum.StrEnum):
    CONFIRMED = "CONFIRMED"
    NEEDS_REVIEW = "NEEDS_REVIEW"


class Evidence(BaseModel):
    speaker: str | None = None
    start_time: int | None = None
    end_time: int | None = None
    quote: str | None = None


class Requirement(BaseModel):
    id: str
    description: str
    type: RequirementType = RequirementType.FUNCTIONAL
    priority: Priority = Priority.MEDIUM
    extraction: Extraction = Extraction.EXPLICIT
    status: RequirementStatus = RequirementStatus.CONFIRMED
    source: Evidence | None = None
    confidence: float = 0.0


class BusinessContext(BaseModel):
    client: str | None = None
    industry: str | None = None
    problem: str = ""
    goals: list[str] = Field(default_factory=list)


class Persona(BaseModel):
    name: str
    description: str = ""


class Constraint(BaseModel):
    description: str
    kind: str = "technical"


class Decision(BaseModel):
    description: str


class Risk(BaseModel):
    description: str


class OpenQuestion(BaseModel):
    question: str


class ActionItem(BaseModel):
    action: str
    owner: str | None = None
    deadline: str | None = None


# ---- list wrappers (structured-output response models must be objects) ----


class RequirementList(BaseModel):
    requirements: list[Requirement] = Field(default_factory=list)


class PersonaList(BaseModel):
    personas: list[Persona] = Field(default_factory=list)


class ConstraintList(BaseModel):
    constraints: list[Constraint] = Field(default_factory=list)


class DecisionList(BaseModel):
    decisions: list[Decision] = Field(default_factory=list)


class RiskList(BaseModel):
    risks: list[Risk] = Field(default_factory=list)


class OpenQuestionList(BaseModel):
    open_questions: list[OpenQuestion] = Field(default_factory=list)


class ActionItemList(BaseModel):
    action_items: list[ActionItem] = Field(default_factory=list)


class MeetingIntelligence(BaseModel):
    business_context: BusinessContext = Field(default_factory=BusinessContext)
    requirements: list[Requirement] = Field(default_factory=list)
    personas: list[Persona] = Field(default_factory=list)
    constraints: list[Constraint] = Field(default_factory=list)
    decisions: list[Decision] = Field(default_factory=list)
    risks: list[Risk] = Field(default_factory=list)
    open_questions: list[OpenQuestion] = Field(default_factory=list)
    action_items: list[ActionItem] = Field(default_factory=list)
    validation_notes: list[str] = Field(default_factory=list)
