"""Meeting Intelligence LangGraph pipeline (Idea.MD §16/§51).

Linear graph: business context → requirements → personas → constraints →
decisions → open questions → risks → evidence validation → synthesize.
"""

from typing import Any, TypedDict

from langgraph.graph import END, START, StateGraph

from app.ai.llm.base import LLMProvider
from app.ai.schemas.intelligence import (
    ActionItem,
    BusinessContext,
    Constraint,
    ConstraintList,
    Decision,
    DecisionList,
    Extraction,
    MeetingIntelligence,
    OpenQuestion,
    OpenQuestionList,
    Persona,
    PersonaList,
    Requirement,
    RequirementList,
    RequirementStatus,
    Risk,
    RiskList,
)

_UNATTRIBUTED = {"", "unknown", "speaker 1", "speaker 2", "speaker"}


class MIState(TypedDict, total=False):
    transcript_text: str
    hint: str | None
    provider: LLMProvider
    thresholds: dict[str, float]
    business_context: BusinessContext
    requirements: list[Requirement]
    personas: list[Persona]
    constraints: list[Constraint]
    decisions: list[Decision]
    risks: list[Risk]
    open_questions: list[OpenQuestion]
    action_items: list[ActionItem]
    validation_notes: list[str]


async def _extract(state: MIState, kind: str, model: type[Any]) -> Any:
    return await state["provider"].extract(
        kind=kind,
        transcript_text=state["transcript_text"],
        response_model=model,
        hint=state.get("hint"),
    )


async def business_context_node(state: MIState) -> dict:
    return {"business_context": await _extract(state, "business_context", BusinessContext)}


async def requirements_node(state: MIState) -> dict:
    result: RequirementList = await _extract(state, "requirements", RequirementList)
    return {"requirements": result.requirements}


async def personas_node(state: MIState) -> dict:
    result: PersonaList = await _extract(state, "personas", PersonaList)
    return {"personas": result.personas}


async def constraints_node(state: MIState) -> dict:
    result: ConstraintList = await _extract(state, "constraints", ConstraintList)
    return {"constraints": result.constraints}


async def decisions_node(state: MIState) -> dict:
    result: DecisionList = await _extract(state, "decisions", DecisionList)
    return {"decisions": result.decisions}


async def open_questions_node(state: MIState) -> dict:
    result: OpenQuestionList = await _extract(state, "open_questions", OpenQuestionList)
    return {"open_questions": result.open_questions}


async def risks_node(state: MIState) -> dict:
    result: RiskList = await _extract(state, "risks", RiskList)
    return {"risks": result.risks}


def evidence_validator_node(state: MIState) -> dict:
    """Verify evidence supports each requirement; flag weak/unattributed/low-confidence
    items as NEEDS_REVIEW (Idea.MD §15, §17)."""
    thresholds = state.get("thresholds", {})
    needs_review = thresholds.get("needs_review", 0.70)
    notes: list[str] = []

    for req in state.get("requirements", []):
        src = req.source
        has_full_evidence = bool(src and src.quote and src.speaker and src.start_time is not None)
        attributed = bool(src and src.speaker and src.speaker.strip().lower() not in _UNATTRIBUTED)

        if req.extraction == Extraction.INFERRED:
            req.status = RequirementStatus.NEEDS_REVIEW
            notes.append(f"{req.id}: inferred — not client-confirmed scope.")
        elif not has_full_evidence:
            req.status = RequirementStatus.NEEDS_REVIEW
            notes.append(f"{req.id}: missing evidence (quote/speaker/timestamp).")
        elif not attributed:
            req.status = RequirementStatus.NEEDS_REVIEW
            notes.append(f"{req.id}: speaker not reliably attributed.")
        elif req.confidence < needs_review:
            req.status = RequirementStatus.NEEDS_REVIEW
            notes.append(f"{req.id}: confidence {req.confidence:.2f} below threshold.")
        else:
            req.status = RequirementStatus.CONFIRMED

    return {"requirements": state.get("requirements", []), "validation_notes": notes}


def synthesize_node(state: MIState) -> dict:
    return {}


def _build_graph():
    g = StateGraph(MIState)
    g.add_node("business_context", business_context_node)
    g.add_node("requirements", requirements_node)
    g.add_node("personas", personas_node)
    g.add_node("constraints", constraints_node)
    g.add_node("decisions", decisions_node)
    g.add_node("open_questions", open_questions_node)
    g.add_node("risks", risks_node)
    g.add_node("evidence_validator", evidence_validator_node)
    g.add_node("synthesize", synthesize_node)

    g.add_edge(START, "business_context")
    g.add_edge("business_context", "requirements")
    g.add_edge("requirements", "personas")
    g.add_edge("personas", "constraints")
    g.add_edge("constraints", "decisions")
    g.add_edge("decisions", "open_questions")
    g.add_edge("open_questions", "risks")
    g.add_edge("risks", "evidence_validator")
    g.add_edge("evidence_validator", "synthesize")
    g.add_edge("synthesize", END)
    return g.compile()


_GRAPH = _build_graph()


async def run_intelligence(
    *,
    transcript_text: str,
    hint: str | None,
    provider: LLMProvider,
    thresholds: dict[str, float],
) -> MeetingIntelligence:
    final: MIState = await _GRAPH.ainvoke(
        {
            "transcript_text": transcript_text,
            "hint": hint,
            "provider": provider,
            "thresholds": thresholds,
        }
    )
    return MeetingIntelligence(
        business_context=final.get("business_context", BusinessContext()),
        requirements=final.get("requirements", []),
        personas=final.get("personas", []),
        constraints=final.get("constraints", []),
        decisions=final.get("decisions", []),
        risks=final.get("risks", []),
        open_questions=final.get("open_questions", []),
        action_items=final.get("action_items", []),
        validation_notes=final.get("validation_notes", []),
    )
