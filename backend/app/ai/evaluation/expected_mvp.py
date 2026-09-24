"""Authored 'expected' MVP for the document-Q&A scenario — deliberately small
(Idea.MD §20/§71). Used by the MockLLMProvider so the MVP pipeline runs offline."""

from app.ai.schemas.mvp import Feature, MVPSpecification, Scope


def build_mvp() -> MVPSpecification:
    return MVPSpecification(
        objective=(
            "Let employees upload documents and get answers to natural-language questions, "
            "with a citation to the source."
        ),
        target_users=["Employees"],
        goals=[
            "Reduce time spent searching internal documents",
            "Provide trustworthy, cited answers",
        ],
        features=[
            Feature(name="Upload PDF documents", scope=Scope.MUST_HAVE),
            Feature(name="Process & chunk documents", scope=Scope.MUST_HAVE),
            Feature(name="Ask natural-language questions", scope=Scope.MUST_HAVE),
            Feature(name="Retrieve relevant passages", scope=Scope.MUST_HAVE),
            Feature(name="Generate answer with citations", scope=Scope.MUST_HAVE),
            Feature(name="Multi-document search", scope=Scope.SHOULD_HAVE),
            Feature(name="Vietnamese document support", scope=Scope.NICE_TO_HAVE),
        ],
        user_journeys=["Upload → Ask → Retrieve → Answer → Cite"],
        acceptance_criteria=[
            "Uploading a PDF makes it searchable",
            "Asking a question returns an answer with at least one citation",
        ],
        out_of_scope=["SSO", "Admin tooling", "Analytics", "CRM integration", "Billing"],
        assumptions=["Single-operator, local data for v1"],
        open_questions=["Expected document volume?"],
        demo_scenario=(
            "Upload HR-Policy.pdf, ask 'What is the annual leave policy?', get a cited answer."
        ),
    )
