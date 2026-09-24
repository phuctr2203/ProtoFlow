"""Demo preparation pipeline (Idea.MD §35-37). A LangGraph node so runs are traced in LangSmith.
Generates the demo narrative (objective, script, synthetic data); the service adds honest,
evidence-derived capability labels. Uses the developer-team LLM, passed in by the caller."""

from typing import TypedDict

from langgraph.graph import END, START, StateGraph

from app.ai.llm.base import LLMProvider
from app.ai.schemas.demo import DemoNarrative


class DemoState(TypedDict, total=False):
    context: str
    provider: LLMProvider
    narrative: DemoNarrative


async def demo_agent_node(state: DemoState) -> dict:
    result = await state["provider"].extract(
        kind="demo",
        transcript_text=state["context"],
        response_model=DemoNarrative,
        hint=None,
    )
    return {"narrative": result}


def _build_graph():
    g = StateGraph(DemoState)
    g.add_node("demo_agent", demo_agent_node)
    g.add_edge(START, "demo_agent")
    g.add_edge("demo_agent", END)
    return g.compile()


_GRAPH = _build_graph()


async def run_demo(*, context: str, provider: LLMProvider) -> DemoNarrative:
    final: DemoState = await _GRAPH.ainvoke({"context": context, "provider": provider})
    return final.get("narrative", DemoNarrative())
