import json
import uuid
from datetime import UTC, datetime

from sqlalchemy import desc, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.ai.graphs.mvp_design import run_design
from app.ai.llm.registry import get_llm_provider
from app.ai.schemas.design import DesignSpec
from app.db.models.design import DesignRecord
from app.db.models.processing import JobStatus, ProcessingJob
from app.domain.mvp.approval import require_approved_mvp


async def generate_design(session: AsyncSession, project_id: uuid.UUID) -> DesignRecord:
    # FR-11 guard: design cannot start without an approved MVP.
    approved = await require_approved_mvp(session, project_id)

    spec: DesignSpec = await run_design(
        mvp_text=json.dumps(approved.data, ensure_ascii=False), provider=get_llm_provider()
    )

    existing = await session.scalar(
        select(DesignRecord).where(
            DesignRecord.project_id == project_id,
            DesignRecord.mvp_version == approved.version,
        )
    )
    payload = spec.model_dump(mode="json")
    if existing is not None:
        existing.data = payload
        record = existing
    else:
        record = DesignRecord(project_id=project_id, mvp_version=approved.version, data=payload)
        session.add(record)

    await session.commit()
    await session.refresh(record)
    return record


async def get_latest_design(session: AsyncSession, project_id: uuid.UUID) -> DesignRecord | None:
    return await session.scalar(
        select(DesignRecord)
        .where(DesignRecord.project_id == project_id)
        .order_by(desc(DesignRecord.created_at))
        .limit(1)
    )


async def run_design_job(session: AsyncSession, project_id: uuid.UUID, job_id: uuid.UUID) -> None:
    job = await session.get(ProcessingJob, job_id)
    if job is None:
        return
    job.status = JobStatus.RUNNING
    job.started_at = datetime.now(UTC)
    job.attempt_count += 1
    await session.commit()

    try:
        await generate_design(session, project_id)
    except Exception as exc:  # noqa: BLE001 - captured to the job record
        job.status = JobStatus.FAILED
        job.error_message = str(exc)
        await session.commit()
        raise

    job.status = JobStatus.COMPLETED
    job.completed_at = datetime.now(UTC)
    await session.commit()
