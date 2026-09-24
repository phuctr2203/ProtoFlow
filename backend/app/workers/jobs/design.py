import uuid

from app.db.database import SessionLocal
from app.db.models.processing import ProcessingJobType
from app.domain.design import service as design_service
from app.domain.meetings.service import create_job


async def process_design(ctx: dict, project_id: str) -> None:
    async with SessionLocal() as session:
        job = await create_job(
            session,
            job_type=ProcessingJobType.MVP_DESIGN,
            project_id=uuid.UUID(project_id),
        )
        await design_service.run_design_job(session, uuid.UUID(project_id), job.id)
