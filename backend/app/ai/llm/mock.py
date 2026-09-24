from pydantic import BaseModel

from app.ai.evaluation.expected import build
from app.ai.schemas.intelligence import (
    ActionItemList,
    ConstraintList,
    DecisionList,
    OpenQuestionList,
    PersonaList,
    RequirementList,
    RiskList,
)


class MockLLMProvider:
    """Deterministic provider used for offline dev and tests. It returns the authored
    'expected' intelligence for the fixture named by `hint` (Idea.MD §78)."""

    name = "mock"

    async def extract(self, *, kind, transcript_text, response_model, hint=None):  # type: ignore[no-untyped-def]
        intel = build(hint or "clean")
        by_kind: dict[str, BaseModel] = {
            "business_context": intel.business_context,
            "requirements": RequirementList(requirements=intel.requirements),
            "personas": PersonaList(personas=intel.personas),
            "constraints": ConstraintList(constraints=intel.constraints),
            "decisions": DecisionList(decisions=intel.decisions),
            "risks": RiskList(risks=intel.risks),
            "open_questions": OpenQuestionList(open_questions=intel.open_questions),
            "action_items": ActionItemList(action_items=intel.action_items),
        }
        result = by_kind.get(kind)
        if result is None:
            return response_model()
        return response_model.model_validate(result.model_dump())
