import uuid
from datetime import UTC, datetime
from typing import Protocol

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models.meeting import (
    Meeting,
    MeetingStatus,
    Transcript,
    TranscriptSegment,
    TranscriptStatus,
)
from app.db.models.processing import (
    JobStatus,
    MeetingEvent,
    MeetingEventStatus,
    ProcessingJob,
    ProcessingJobType,
)
from app.integrations.meetings.base import TranscriptData
from app.integrations.meetings.registry import get_provider


class MeetingNotFoundError(Exception):
    def __init__(self, meeting_id: uuid.UUID) -> None:
        super().__init__(f"Meeting {meeting_id} not found")
        self.meeting_id = meeting_id


async def create_meeting(
    session: AsyncSession,
    *,
    project_id: uuid.UUID,
    external_meeting_id: str,
    title: str,
    provider: str = "mock",
    status: MeetingStatus = MeetingStatus.COMPLETED,
) -> Meeting:
    meeting = Meeting(
        project_id=project_id,
        provider=provider,
        external_meeting_id=external_meeting_id,
        title=title,
        status=status,
    )
    session.add(meeting)
    await session.commit()
    await session.refresh(meeting)
    return meeting


async def list_meetings(
    session: AsyncSession, project_id: uuid.UUID | None = None
) -> list[Meeting]:
    stmt = select(Meeting).order_by(Meeting.created_at.desc())
    if project_id is not None:
        stmt = stmt.where(Meeting.project_id == project_id)
    result = await session.execute(stmt)
    return list(result.scalars().all())


async def record_event(
    session: AsyncSession,
    *,
    provider: str,
    event_type: str,
    external_event_id: str,
    meeting_id: uuid.UUID | None,
    payload: dict,
) -> tuple[MeetingEvent, bool]:
    """Persist a meeting event idempotently.

    Returns (event, created). The idempotency key is (provider, external_event_id):
    a redelivered event returns the existing row with created=False.
    """
    existing = await session.scalar(
        select(MeetingEvent).where(
            MeetingEvent.provider == provider,
            MeetingEvent.external_event_id == external_event_id,
        )
    )
    if existing is not None:
        return existing, False

    event = MeetingEvent(
        provider=provider,
        event_type=event_type,
        external_event_id=external_event_id,
        meeting_id=meeting_id,
        payload=payload,
        status=MeetingEventStatus.QUEUED,
    )
    session.add(event)
    try:
        await session.commit()
    except IntegrityError:
        await session.rollback()
        existing = await session.scalar(
            select(MeetingEvent).where(
                MeetingEvent.provider == provider,
                MeetingEvent.external_event_id == external_event_id,
            )
        )
        assert existing is not None
        return existing, False

    await session.refresh(event)
    return event, True


async def create_job(
    session: AsyncSession,
    *,
    job_type: ProcessingJobType,
    meeting_id: uuid.UUID | None = None,
    project_id: uuid.UUID | None = None,
) -> ProcessingJob:
    job = ProcessingJob(job_type=job_type, meeting_id=meeting_id, project_id=project_id)
    session.add(job)
    await session.commit()
    await session.refresh(job)
    return job


def _normalize(data: TranscriptData) -> tuple[list[TranscriptSegment], str]:
    ordered = sorted(data.segments, key=lambda s: s.start_time)
    segments: list[TranscriptSegment] = []
    lines: list[str] = []
    for seq, seg in enumerate(ordered):
        text = seg.text.strip()
        segments.append(
            TranscriptSegment(
                seq=seq,
                speaker=seg.speaker.strip(),
                start_time=seg.start_time,
                end_time=seg.end_time,
                text=text,
            )
        )
        lines.append(f"{seg.speaker.strip()}: {text}")
    return segments, "\n".join(lines)


async def process_transcript(session: AsyncSession, meeting_id: uuid.UUID) -> Transcript:
    """Fetch the transcript via the provider, normalize it, and advance the meeting
    to TRANSCRIPT_READY (Idea.MD §62)."""
    meeting = await session.get(Meeting, meeting_id)
    if meeting is None:
        raise MeetingNotFoundError(meeting_id)

    provider = get_provider(meeting.provider)
    data = await provider.get_transcript(meeting.external_meeting_id)
    segments, normalized = _normalize(data)

    transcript = Transcript(
        meeting_id=meeting.id,
        raw_content=normalized,
        normalized_content=normalized,
        language=data.language,
        status=TranscriptStatus.NORMALIZED,
        segments=segments,
    )
    session.add(transcript)
    meeting.status = MeetingStatus.TRANSCRIPT_READY
    await session.commit()
    await session.refresh(transcript)
    return transcript


async def run_transcript_job(
    session: AsyncSession, meeting_id: uuid.UUID, job_id: uuid.UUID
) -> None:
    """Job orchestration: mark the job/event lifecycle around process_transcript
    with retry-friendly failure capture (Idea.MD §76, NFR2)."""
    job = await session.get(ProcessingJob, job_id)
    if job is None:
        return
    job.status = JobStatus.RUNNING
    job.started_at = datetime.now(UTC)
    job.attempt_count += 1
    await session.commit()

    try:
        await process_transcript(session, meeting_id)
    except Exception as exc:  # noqa: BLE001 - captured to the job record
        job.status = JobStatus.FAILED
        job.error_message = str(exc)
        await session.commit()
        raise

    job.status = JobStatus.COMPLETED
    job.completed_at = datetime.now(UTC)
    await session.commit()


class QueueLike(Protocol):
    async def enqueue_job(self, function: str, *args: object) -> object: ...


async def get_meeting_by_external(
    session: AsyncSession, provider: str, external_meeting_id: str
) -> Meeting | None:
    return await session.scalar(
        select(Meeting).where(
            Meeting.provider == provider,
            Meeting.external_meeting_id == external_meeting_id,
        )
    )


async def handle_transcript_ready(
    session: AsyncSession,
    queue: QueueLike,
    *,
    provider: str,
    external_event_id: str,
    external_meeting_id: str,
    event_type: str = "transcript.ready",
    payload: dict | None = None,
) -> dict:
    """Lightweight webhook path (Idea.MD §49): validate → persist event (idempotent)
    → queue job → return. No long-running work is done inline."""
    meeting = await get_meeting_by_external(session, provider, external_meeting_id)
    if meeting is None:
        raise MeetingNotFoundError(external_meeting_id)  # type: ignore[arg-type]

    event, created = await record_event(
        session,
        provider=provider,
        event_type=event_type,
        external_event_id=external_event_id,
        meeting_id=meeting.id,
        payload=payload or {},
    )
    if not created:
        return {"status": "duplicate", "event_id": str(event.id), "meeting_id": str(meeting.id)}

    job = await create_job(
        session,
        job_type=ProcessingJobType.TRANSCRIPT_PROCESSING,
        meeting_id=meeting.id,
        project_id=meeting.project_id,
    )
    meeting.status = MeetingStatus.TRANSCRIPT_PENDING
    await session.commit()

    await queue.enqueue_job("process_transcript", str(meeting.id), str(job.id))
    return {
        "status": "queued",
        "event_id": str(event.id),
        "meeting_id": str(meeting.id),
        "job_id": str(job.id),
    }
