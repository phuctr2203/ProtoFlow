"""Authored 'expected' Meeting Intelligence for each mock transcript fixture.

This doubles as the evaluation ground truth (Idea.MD §78) and as the deterministic
output the MockLLMProvider returns, so the pipeline runs and is testable offline.
Noise profiles carry weaker evidence / lower confidence so the Evidence Validator
genuinely flags NEEDS_REVIEW rather than only seeing a clean happy path.
"""

from app.ai.schemas.intelligence import (
    ActionItem,
    BusinessContext,
    Constraint,
    Decision,
    Evidence,
    Extraction,
    MeetingIntelligence,
    OpenQuestion,
    Persona,
    Priority,
    Requirement,
    RequirementType,
    Risk,
)

# Per-profile tuning: (confidence, speaker used in evidence, garble the quotes?)
_PROFILE = {
    "clean": {"conf": 0.97, "speaker": "Client", "attributed": True},
    "asr_noisy": {"conf": 0.74, "speaker": "Client", "attributed": True},
    "diarization_noisy": {"conf": 0.82, "speaker": "Unknown", "attributed": False},
    "mixed_language": {"conf": 0.85, "speaker": "Client", "attributed": True},
    "combined": {"conf": 0.62, "speaker": "Speaker 1", "attributed": False},
}

_BASE_REQS = [
    (
        "REQ-001",
        "Users can upload PDF documents.",
        Priority.HIGH,
        "Most of our documents are PDF.",
        725,
        730,
    ),
    (
        "REQ-002",
        "Users can ask questions in natural language.",
        Priority.HIGH,
        "We want employees to ask questions in natural language.",
        1102,
        1115,
    ),
    (
        "REQ-003",
        "Answers must show source citations.",
        Priority.HIGH,
        "The answer should show its source.",
        1123,
        1130,
    ),
    (
        "REQ-004",
        "Provide a simple interface for the first demo.",
        Priority.MEDIUM,
        "For the first demo we only need a simple interface.",
        1500,
        1508,
    ),
]


def build(profile: str) -> MeetingIntelligence:
    cfg = _PROFILE.get(profile, _PROFILE["clean"])
    conf = float(cfg["conf"])
    speaker = str(cfg["speaker"]) if cfg["attributed"] else str(cfg["speaker"])

    requirements: list[Requirement] = []
    for rid, desc, prio, quote, start, end in _BASE_REQS:
        requirements.append(
            Requirement(
                id=rid,
                description=desc,
                type=RequirementType.FUNCTIONAL,
                priority=prio,
                extraction=Extraction.EXPLICIT,
                source=Evidence(speaker=speaker, start_time=start, end_time=end, quote=quote),
                confidence=conf,
            )
        )

    # An inferred requirement — never presented as client-confirmed scope (Idea.MD §15).
    requirements.append(
        Requirement(
            id="REQ-005",
            description="A document processing / chunking pipeline is required.",
            type=RequirementType.FUNCTIONAL,
            priority=Priority.MEDIUM,
            extraction=Extraction.INFERRED,
            source=None,
            confidence=0.6,
        )
    )

    if profile in {"mixed_language", "combined"}:
        requirements.append(
            Requirement(
                id="REQ-006",
                description="Support documents written in Vietnamese.",
                type=RequirementType.FUNCTIONAL,
                priority=Priority.MEDIUM,
                extraction=Extraction.EXPLICIT,
                source=Evidence(
                    speaker=speaker, start_time=89, end_time=96, quote="một số bằng tiếng Việt"
                ),
                confidence=0.68,
            )
        )

    return MeetingIntelligence(
        business_context=BusinessContext(
            client="Acme Corp",
            problem="Employees waste too much time searching hundreds of internal documents.",
            goals=[
                "Let employees find information via natural-language Q&A",
                "Show sources for every answer",
            ],
        ),
        requirements=requirements,
        personas=[Persona(name="Employee", description="Searches internal documents for answers.")],
        constraints=[Constraint(description="Documents are mostly PDF.", kind="data")],
        decisions=[
            Decision(description="Start with a simple interface for the first demo."),
            Decision(description="PDF is the primary document format."),
        ],
        risks=[Risk(description="Hallucinated answers if citations are not enforced.")],
        open_questions=[
            OpenQuestion(question="Expected document volume?"),
            OpenQuestion(question="Who maintains the knowledge base?"),
            OpenQuestion(question="Is access control required for v1?"),
        ],
        action_items=[ActionItem(action="Share a sample set of documents", owner="Client")],
    )
