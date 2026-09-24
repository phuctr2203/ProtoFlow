import uuid

from app.db.database import SessionLocal
from app.domain.meetings import service


async def process_transcript(ctx: dict, meeting_id: str, job_id: str) -> None:
    async with SessionLocal() as session:
        await service.run_transcript_job(session, uuid.UUID(meeting_id), uuid.UUID(job_id))

    # Chain: once the transcript is ready, kick off meeting intelligence (Idea.MD §62 → §63).
    redis = ctx.get("redis")
    if redis is not None:
        await redis.enqueue_job("process_meeting_intelligence", meeting_id)
