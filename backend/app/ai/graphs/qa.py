"""QA test-generation pipeline (Idea.MD §33). A LangGraph node so runs are traced in LangSmith.
Uses the developer-team LLM (get_dev_llm_provider), passed in by the caller."""

from typing import TypedDict

from langgraph.graph import END, START, StateGraph

from app.ai.llm.base import LLMProvider
from app.ai.schemas.qa import TestCaseList


class QAState(TypedDict, total=False):
    mvp_text: str
    provider: LLMProvider
    test_cases: TestCaseList


async def qa_agent_node(state: QAState) -> dict:
    result = await state["provider"].extract(
        kind="qa_test_cases",
        transcript_text=state["mvp_text"],
        response_model=TestCaseList,
        hint=None,
    )
    return {"test_cases": result}


def _build_graph():
    g = StateGraph(QAState)
    g.add_node("qa_agent", qa_agent_node)
    g.add_edge(START, "qa_agent")
    g.add_edge("qa_agent", END)
    return g.compile()


_GRAPH = _build_graph()


async def run_qa(*, mvp_text: str, provider: LLMProvider) -> TestCaseList:
    final: QAState = await _GRAPH.ainvoke({"mvp_text": mvp_text, "provider": provider})
    return final.get("test_cases", TestCaseList())
