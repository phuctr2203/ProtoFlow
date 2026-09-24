import uuid

from app.db.database import SessionLocal
from app.db.models.processing import ProcessingJobType
from app.domain.intelligence import service as intel_service
from app.domain.meetings.service import create_job


async def process_meeting_intelligence(ctx: dict, meeting_id: str) -> None:
    async with SessionLocal() as session:
        job = await create_job(
            session,
            job_type=ProcessingJobType.MEETING_INTELLIGENCE,
            meeting_id=uuid.UUID(meeting_id),
        )
        await intel_service.run_meeting_intelligence_job(session, uuid.UUID(meeting_id), job.id)
