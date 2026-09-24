import uuid

from app.db.database import SessionLocal
from app.db.models.processing import ProcessingJobType
from app.domain.development import service as development_service
from app.domain.meetings.service import create_job


async def process_code_generation(ctx: dict, project_id: str) -> None:
    """CODE_GENERATION job (Epic 6): the Development Manager breaks the approved, designed MVP into
    an ordered task list, then the configured coding engine implements it in a workspace
    (Stories 6.1 + 6.3). Story 6.4 will open a PR from the result."""
    async with SessionLocal() as session:
        job = await create_job(
            session,
            job_type=ProcessingJobType.CODE_GENERATION,
            project_id=uuid.UUID(project_id),
        )
        await development_service.run_code_generation_job(session, uuid.UUID(project_id), job.id)
