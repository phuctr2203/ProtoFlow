import uuid

from app.db.database import SessionLocal
from app.db.models.processing import ProcessingJobType
from app.domain.meetings.service import create_job
from app.domain.qa import service as qa_service


async def process_qa(ctx: dict, project_id: str) -> None:
    """QA job (Epic 7): generate tests from the MVP's requirements/acceptance criteria, record
    results, and roll up requirement coverage (FR-16, FR-17)."""
    async with SessionLocal() as session:
        job = await create_job(
            session,
            job_type=ProcessingJobType.QA,
            project_id=uuid.UUID(project_id),
        )
        await qa_service.run_qa_job(session, uuid.UUID(project_id), job.id)
