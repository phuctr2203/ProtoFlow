import uuid

from app.db.database import SessionLocal
from app.db.models.processing import ProcessingJobType
from app.domain.demo import service as demo_service
from app.domain.meetings.service import create_job


async def process_demo(ctx: dict, project_id: str) -> None:
    """DEMO_PREPARATION job (Epic 8): generate an honest demo package (objective, script, synthetic
    data, IMPLEMENTED/SIMULATED/NOT_IMPLEMENTED labels) from the MVP + QA (FR-18, FR-19)."""
    async with SessionLocal() as session:
        job = await create_job(
            session,
            job_type=ProcessingJobType.DEMO_PREPARATION,
            project_id=uuid.UUID(project_id),
        )
        await demo_service.run_demo_job(session, uuid.UUID(project_id), job.id)
