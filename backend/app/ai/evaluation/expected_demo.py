"""Authored 'expected' demo narrative for the document-Q&A MVP (Idea.MD §35-37). Used by the
MockLLMProvider so the demo pipeline runs offline. Capability labels are added by the service from
QA evidence, not here."""

from app.ai.schemas.demo import DemoNarrative, DemoStep


def build_demo() -> DemoNarrative:
    return DemoNarrative(
        objective="Show asking questions of an uploaded document and getting cited answers.",
        script=[
            DemoStep(order=1, action="Upload the sample contract PDF", expected="Document listed"),
            DemoStep(order=2, action="Wait for indexing", expected="Status shows 'Indexed'"),
            DemoStep(order=3, action="Ask a question about the contract", expected="Cited answer"),
            DemoStep(order=4, action="Open a citation", expected="Source passage highlighted"),
        ],
        synthetic_data=[
            "SYNTHETIC: sample_contract.pdf (fictional vendor agreement)",
            "SYNTHETIC: 3 example questions about the contract",
        ],
        known_limitations=[
            "Multi-document search is not yet implemented",
            "Vietnamese document support is not yet implemented",
        ],
        next_steps=[
            "Add multi-document search",
            "Add authentication and per-user document scoping",
        ],
    )
