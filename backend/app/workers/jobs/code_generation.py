import uuid

from app.db.database import SessionLocal
from app.db.models.processing import ProcessingJobType
from app.domain.development import service as development_service
from app.domain.meetings.service import create_job


async def process_code_generation(ctx: dict, project_id: str) -> None:
    """CODE_GENERATION job (Epic 6). Phase 1 (Story 6.1): the Development Manager breaks the
    approved, designed MVP into an ordered task list. Story 6.3 will extend this job to have
    the coding agents implement those tasks via the Claude Agent SDK and open a PR."""
    async with SessionLocal() as session:
        job = await create_job(
            session,
            job_type=ProcessingJobType.CODE_GENERATION,
            project_id=uuid.UUID(project_id),
        )
        await development_service.run_development_job(session, uuid.UUID(project_id), job.id)
