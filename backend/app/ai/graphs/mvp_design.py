"""MVP Design pipeline (Idea.MD §24-26): UX Agent → Solution Design Agent.
Deliberately lightweight — a 1-5 page equivalent, not a heavy architecture doc."""

from typing import Any, TypedDict

from langgraph.graph import END, START, StateGraph

from app.ai.llm.base import LLMProvider
from app.ai.schemas.design import DesignSpec, SolutionDesign, UXDesign


class DesignState(TypedDict, total=False):
    mvp_text: str
    provider: LLMProvider
    ux: UXDesign
    solution: SolutionDesign


async def _extract(state: DesignState, kind: str, model: type[Any]) -> Any:
    return await state["provider"].extract(
        kind=kind, transcript_text=state["mvp_text"], response_model=model, hint=None
    )


async def ux_agent_node(state: DesignState) -> dict:
    return {"ux": await _extract(state, "design_ux", UXDesign)}


async def solution_design_node(state: DesignState) -> dict:
    return {"solution": await _extract(state, "design_solution", SolutionDesign)}


def synthesize_node(state: DesignState) -> dict:
    return {}


def _build_graph():
    g = StateGraph(DesignState)
    g.add_node("ux_agent", ux_agent_node)
    g.add_node("solution_design", solution_design_node)
    g.add_node("synthesize", synthesize_node)
    g.add_edge(START, "ux_agent")
    g.add_edge("ux_agent", "solution_design")
    g.add_edge("solution_design", "synthesize")
    g.add_edge("synthesize", END)
    return g.compile()


_GRAPH = _build_graph()


async def run_design(*, mvp_text: str, provider: LLMProvider) -> DesignSpec:
    final: DesignState = await _GRAPH.ainvoke({"mvp_text": mvp_text, "provider": provider})
    ux = final.get("ux", UXDesign())
    solution = final.get("solution", SolutionDesign())
    return DesignSpec(
        user_journey=ux.user_journey,
        screens=ux.screens,
        navigation=ux.navigation,
        ui_states=ux.ui_states,
        components=solution.components,
        apis=solution.apis,
        data_model=solution.data_model,
        ai_workflow=solution.ai_workflow,
        tech_decisions=solution.tech_decisions,
    )
