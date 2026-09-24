"""MVP Definition agent-team pipeline (Idea.MD §18/§51).

Product Manager → Feature Analyst → UX Analyst → Scope Analyst → Critic →
Synthesizer. The Scope Analyst enforces smallness; the result is intentionally
MVP-sized, not a full PRD (NFR7).
"""

from typing import Any, TypedDict

from langgraph.graph import END, START, StateGraph

from app.ai.llm.base import LLMProvider
from app.ai.schemas.mvp import (
    Critique,
    Feature,
    FeatureList,
    MVPCore,
    MVPSpecification,
    Scope,
    UXPlan,
)

_MAX_SHOULD_HAVE = 2


class MVPState(TypedDict, total=False):
    intelligence_text: str
    provider: LLMProvider
    core: MVPCore
    features: list[Feature]
    ux: UXPlan
    critique: Critique
    out_of_scope: list[str]


async def _extract(state: MVPState, kind: str, model: type[Any]) -> Any:
    return await state["provider"].extract(
        kind=kind, transcript_text=state["intelligence_text"], response_model=model, hint=None
    )


async def product_manager_node(state: MVPState) -> dict:
    return {"core": await _extract(state, "mvp_pm", MVPCore)}


async def feature_analyst_node(state: MVPState) -> dict:
    result: FeatureList = await _extract(state, "mvp_features", FeatureList)
    return {"features": result.features}


async def ux_analyst_node(state: MVPState) -> dict:
    return {"ux": await _extract(state, "mvp_ux", UXPlan)}


def scope_analyst_node(state: MVPState) -> dict:
    """Aggressively reduce scope: keep MUST_HAVE, cap SHOULD_HAVE, demote extra
    NICE_TO_HAVE to OUT_OF_SCOPE so the MVP stays demoable (Idea.MD §21, NFR7)."""
    features = state.get("features", [])
    kept: list[Feature] = []
    demoted: list[str] = []
    should_count = 0
    for f in features:
        if f.scope == Scope.MUST_HAVE:
            kept.append(f)
        elif f.scope == Scope.SHOULD_HAVE and should_count < _MAX_SHOULD_HAVE:
            kept.append(f)
            should_count += 1
        else:
            demoted.append(f.name)
    return {"features": kept, "out_of_scope": demoted}


async def critic_node(state: MVPState) -> dict:
    return {"critique": await _extract(state, "mvp_critique", Critique)}


def synthesize_node(state: MVPState) -> dict:
    return {}


def _build_graph():
    g = StateGraph(MVPState)
    g.add_node("product_manager", product_manager_node)
    g.add_node("feature_analyst", feature_analyst_node)
    g.add_node("ux_analyst", ux_analyst_node)
    g.add_node("scope_analyst", scope_analyst_node)
    g.add_node("critic", critic_node)
    g.add_node("synthesize", synthesize_node)

    g.add_edge(START, "product_manager")
    g.add_edge("product_manager", "feature_analyst")
    g.add_edge("feature_analyst", "ux_analyst")
    g.add_edge("ux_analyst", "scope_analyst")
    g.add_edge("scope_analyst", "critic")
    g.add_edge("critic", "synthesize")
    g.add_edge("synthesize", END)
    return g.compile()


_GRAPH = _build_graph()


async def run_mvp_definition(*, intelligence_text: str, provider: LLMProvider) -> MVPSpecification:
    final: MVPState = await _GRAPH.ainvoke(
        {"intelligence_text": intelligence_text, "provider": provider}
    )
    core = final.get("core", MVPCore())
    ux = final.get("ux", UXPlan())
    critique = final.get("critique", Critique())
    out_of_scope = list(dict.fromkeys(critique.out_of_scope + final.get("out_of_scope", [])))

    return MVPSpecification(
        objective=core.objective,
        target_users=core.target_users,
        goals=core.goals,
        features=final.get("features", []),
        user_journeys=ux.user_journeys,
        acceptance_criteria=ux.acceptance_criteria,
        out_of_scope=out_of_scope,
        assumptions=critique.assumptions,
        open_questions=critique.open_questions,
        demo_scenario=ux.demo_scenario,
    )
