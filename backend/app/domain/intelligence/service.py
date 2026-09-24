import uuid
from datetime import UTC, datetime

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.ai.graphs.meeting_intelligence import run_intelligence
from app.ai.llm.registry import get_llm_provider
from app.ai.schemas.intelligence import MeetingIntelligence
from app.core.config import settings
from app.db.models.intelligence import MeetingIntelligenceRecord
from app.db.models.meeting import Meeting, MeetingStatus, Transcript
from app.db.models.processing import JobStatus, ProcessingJob
from app.domain.meetings.service import MeetingNotFoundError


async def run_meeting_intelligence(
    session: AsyncSession, meeting_id: uuid.UUID
) -> MeetingIntelligence:
    meeting = await session.get(Meeting, meeting_id)
    if meeting is None:
        raise MeetingNotFoundError(meeting_id)

    transcript = await session.scalar(
        select(Transcript)
        .where(Transcript.meeting_id == meeting_id)
        .options(selectinload(Transcript.segments))
    )
    if transcript is None:
        raise ValueError(f"Meeting {meeting_id} has no transcript yet")

    text = transcript.normalized_content or "\n".join(
        f"{s.speaker}: {s.text}" for s in transcript.segments
    )

    intel = await run_intelligence(
        transcript_text=text,
        hint=meeting.external_meeting_id,
        provider=get_llm_provider(),
        thresholds={
            "high": settings.confidence_high,
            "needs_review": settings.confidence_needs_review,
        },
    )

    payload = intel.model_dump(mode="json")
    existing = await session.scalar(
        select(MeetingIntelligenceRecord).where(MeetingIntelligenceRecord.meeting_id == meeting_id)
    )
    if existing is not None:
        existing.data = payload
    else:
        session.add(MeetingIntelligenceRecord(meeting_id=meeting_id, data=payload))

    meeting.status = MeetingStatus.PROCESSED
    await session.commit()
    return intel


async def get_intelligence(
    session: AsyncSession, meeting_id: uuid.UUID
) -> MeetingIntelligenceRecord | None:
    return await session.scalar(
        select(MeetingIntelligenceRecord).where(MeetingIntelligenceRecord.meeting_id == meeting_id)
    )


async def run_meeting_intelligence_job(
    session: AsyncSession, meeting_id: uuid.UUID, job_id: uuid.UUID
) -> None:
    job = await session.get(ProcessingJob, job_id)
    if job is None:
        return
    job.status = JobStatus.RUNNING
    job.started_at = datetime.now(UTC)
    job.attempt_count += 1
    await session.commit()

    try:
        await run_meeting_intelligence(session, meeting_id)
    except Exception as exc:  # noqa: BLE001 - captured to the job record
        job.status = JobStatus.FAILED
        job.error_message = str(exc)
        await session.commit()
        raise

    job.status = JobStatus.COMPLETED
    job.completed_at = datetime.now(UTC)
    await session.commit()
