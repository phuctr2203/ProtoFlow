"""Development Manager pipeline (Idea.MD §28, §30): turn an approved, designed MVP into
an ordered development task list. A LangGraph node so runs are traced in LangSmith.

Uses the developer-team LLM (get_dev_llm_provider), passed in by the caller."""

from typing import TypedDict

from langgraph.graph import END, START, StateGraph

from app.ai.llm.base import LLMProvider
from app.ai.schemas.development import DevelopmentPlan


class DevPlanState(TypedDict, total=False):
    mvp_text: str
    design_text: str
    provider: LLMProvider
    plan: DevelopmentPlan


async def development_manager_node(state: DevPlanState) -> dict:
    context = state["mvp_text"]
    if state.get("design_text"):
        context = f"{context}\n\n--- DESIGN ---\n{state['design_text']}"
    plan = await state["provider"].extract(
        kind="development_tasks",
        transcript_text=context,
        response_model=DevelopmentPlan,
        hint=None,
    )
    return {"plan": plan}


def _build_graph():
    g = StateGraph(DevPlanState)
    g.add_node("development_manager", development_manager_node)
    g.add_edge(START, "development_manager")
    g.add_edge("development_manager", END)
    return g.compile()


_GRAPH = _build_graph()


async def run_development_plan(
    *, mvp_text: str, design_text: str, provider: LLMProvider
) -> DevelopmentPlan:
    final: DevPlanState = await _GRAPH.ainvoke(
        {"mvp_text": mvp_text, "design_text": design_text, "provider": provider}
    )
    return final.get("plan", DevelopmentPlan())
