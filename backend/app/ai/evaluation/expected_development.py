"""Authored 'expected' development plan for the document-Q&A MVP (Idea.MD §28-30).
Used by the MockLLMProvider so the Development Manager runs offline. Kept small and ordered."""

from app.ai.schemas.development import DevelopmentPlan, DevelopmentTask


def build_development() -> DevelopmentPlan:
    return DevelopmentPlan(
        tasks=[
            DevelopmentTask(
                id="TASK-001",
                title="Provision vector DB and object storage",
                description="Wire Qdrant and MinIO clients and health checks.",
                component="infra",
                depends_on=[],
                order=1,
            ),
            DevelopmentTask(
                id="TASK-002",
                title="Document upload API and storage",
                description="POST /documents stores the file in MinIO and records metadata.",
                component="backend",
                depends_on=["TASK-001"],
                order=2,
            ),
            DevelopmentTask(
                id="TASK-003",
                title="Ingestion pipeline: extract, chunk, embed, index",
                description="Extract text, chunk, embed, and upsert vectors into Qdrant.",
                component="ai",
                depends_on=["TASK-002"],
                order=3,
            ),
            DevelopmentTask(
                id="TASK-004",
                title="Ask API with retrieval and citations",
                description="POST /ask retrieves relevant chunks and answers with citations.",
                component="backend",
                depends_on=["TASK-003"],
                order=4,
            ),
            DevelopmentTask(
                id="TASK-005",
                title="Upload and chat UI",
                description="Upload dropzone, chat input, and answer card with citation chips.",
                component="frontend",
                depends_on=["TASK-002", "TASK-004"],
                order=5,
            ),
        ]
    )
