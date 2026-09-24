import uuid

from app.db.database import SessionLocal
from app.domain.meetings import service


async def process_transcript(ctx: dict, meeting_id: str, job_id: str) -> None:
    async with SessionLocal() as session:
        await service.run_transcript_job(session, uuid.UUID(meeting_id), uuid.UUID(job_id))
