from pydantic import BaseModel

from app.ai.evaluation.expected import build
from app.ai.evaluation.expected_mvp import build_mvp
from app.ai.schemas.intelligence import (
    ActionItemList,
    ConstraintList,
    DecisionList,
    OpenQuestionList,
    PersonaList,
    RequirementList,
    RiskList,
)
from app.ai.schemas.mvp import Critique, FeatureList, MVPCore, UXPlan


class MockLLMProvider:
    """Deterministic provider used for offline dev and tests. It returns authored
    'expected' output for the fixture named by `hint` (Idea.MD §78)."""

    name = "mock"

    async def extract(self, *, kind, transcript_text, response_model, hint=None):  # type: ignore[no-untyped-def]
        by_kind: dict[str, BaseModel]
        if kind.startswith("mvp"):
            mvp = build_mvp()
            by_kind = {
                "mvp_pm": MVPCore(
                    objective=mvp.objective, target_users=mvp.target_users, goals=mvp.goals
                ),
                "mvp_features": FeatureList(features=mvp.features),
                "mvp_ux": UXPlan(
                    user_journeys=mvp.user_journeys,
                    acceptance_criteria=mvp.acceptance_criteria,
                    demo_scenario=mvp.demo_scenario,
                ),
                "mvp_critique": Critique(
                    out_of_scope=mvp.out_of_scope,
                    assumptions=mvp.assumptions,
                    open_questions=mvp.open_questions,
                ),
            }
        else:
            intel = build(hint or "clean")
            by_kind = {
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
