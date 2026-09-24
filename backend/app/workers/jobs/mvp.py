import uuid

from app.db.database import SessionLocal
from app.db.models.processing import ProcessingJobType
from app.domain.meetings.service import create_job
from app.domain.mvp import service as mvp_service


async def process_mvp(ctx: dict, project_id: str) -> None:
    async with SessionLocal() as session:
        job = await create_job(
            session,
            job_type=ProcessingJobType.MVP_ANALYSIS,
            project_id=uuid.UUID(project_id),
        )
        await mvp_service.run_mvp_job(session, uuid.UUID(project_id), job.id)
