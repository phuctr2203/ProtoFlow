import json
import uuid
from datetime import UTC, datetime

from sqlalchemy import desc, func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.ai.graphs.mvp_definition import run_mvp_definition
from app.ai.llm.registry import get_llm_provider
from app.ai.schemas.mvp import MVPSpecification
from app.db.models.intelligence import MeetingIntelligenceRecord
from app.db.models.meeting import Meeting
from app.db.models.mvp import MVPSpecificationRecord, MVPStatus
from app.db.models.processing import JobStatus, ProcessingJob
from app.db.models.project import Project, ProjectStatus


class NoIntelligenceError(Exception):
    """Raised when a project has no processed meeting intelligence to build an MVP from."""


async def _latest_intelligence_text(session: AsyncSession, project_id: uuid.UUID) -> str:
    record = await session.scalar(
        select(MeetingIntelligenceRecord)
        .join(Meeting, Meeting.id == MeetingIntelligenceRecord.meeting_id)
        .where(Meeting.project_id == project_id)
        .order_by(desc(MeetingIntelligenceRecord.created_at))
        .limit(1)
    )
    if record is None:
        raise NoIntelligenceError(f"Project {project_id} has no meeting intelligence yet")
    return json.dumps(record.data, ensure_ascii=False)


async def generate_mvp(session: AsyncSession, project_id: uuid.UUID) -> MVPSpecificationRecord:
    intelligence_text = await _latest_intelligence_text(session, project_id)
    spec: MVPSpecification = await run_mvp_definition(
        intelligence_text=intelligence_text, provider=get_llm_provider()
    )

    last_version = await session.scalar(
        select(func.max(MVPSpecificationRecord.version)).where(
            MVPSpecificationRecord.project_id == project_id
        )
    )
    record = MVPSpecificationRecord(
        project_id=project_id,
        version=(last_version or 0) + 1,
        status=MVPStatus.DRAFT,
        data=spec.model_dump(mode="json"),
    )
    session.add(record)

    project = await session.get(Project, project_id)
    if project is not None and project.status == ProjectStatus.DISCOVERY:
        project.status = ProjectStatus.MVP_DEFINITION

    await session.commit()
    await session.refresh(record)
    return record


async def get_latest_mvp(
    session: AsyncSession, project_id: uuid.UUID
) -> MVPSpecificationRecord | None:
    return await session.scalar(
        select(MVPSpecificationRecord)
        .where(MVPSpecificationRecord.project_id == project_id)
        .order_by(desc(MVPSpecificationRecord.version))
        .limit(1)
    )


async def list_mvps(session: AsyncSession, project_id: uuid.UUID) -> list[MVPSpecificationRecord]:
    result = await session.execute(
        select(MVPSpecificationRecord)
        .where(MVPSpecificationRecord.project_id == project_id)
        .order_by(desc(MVPSpecificationRecord.version))
    )
    return list(result.scalars().all())


async def run_mvp_job(session: AsyncSession, project_id: uuid.UUID, job_id: uuid.UUID) -> None:
    job = await session.get(ProcessingJob, job_id)
    if job is None:
        return
    job.status = JobStatus.RUNNING
    job.started_at = datetime.now(UTC)
    job.attempt_count += 1
    await session.commit()

    try:
        await generate_mvp(session, project_id)
    except Exception as exc:  # noqa: BLE001 - captured to the job record
        job.status = JobStatus.FAILED
        job.error_message = str(exc)
        await session.commit()
        raise

    job.status = JobStatus.COMPLETED
    job.completed_at = datetime.now(UTC)
    await session.commit()
