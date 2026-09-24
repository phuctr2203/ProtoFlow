import json
import uuid
from datetime import UTC, datetime

from sqlalchemy import desc, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.ai.graphs.development_plan import run_development_plan
from app.ai.llm.registry import get_dev_llm_provider
from app.ai.schemas.development import DevelopmentPlan
from app.db.models.development import DevelopmentPlanRecord
from app.db.models.processing import JobStatus, ProcessingJob
from app.domain.design import service as design_service
from app.domain.mvp.approval import require_approved_mvp


class DesignNotReadyError(Exception):
    """Raised when development planning is attempted before a design exists (Epic 6 ← Epic 5)."""


async def generate_development_plan(
    session: AsyncSession, project_id: uuid.UUID
) -> DevelopmentPlanRecord:
    # Epic 6 depends on an approved MVP (FR-11) and its design (Epic 5).
    approved = await require_approved_mvp(session, project_id)
    design = await design_service.get_latest_design(session, project_id)
    if design is None:
        raise DesignNotReadyError(
            f"Project {project_id} has no design yet; generate the design before development."
        )

    plan: DevelopmentPlan = await run_development_plan(
        mvp_text=json.dumps(approved.data, ensure_ascii=False),
        design_text=json.dumps(design.data, ensure_ascii=False),
        provider=get_dev_llm_provider(),
    )

    existing = await session.scalar(
        select(DevelopmentPlanRecord).where(
            DevelopmentPlanRecord.project_id == project_id,
            DevelopmentPlanRecord.mvp_version == approved.version,
        )
    )
    payload = plan.model_dump(mode="json")
    if existing is not None:
        existing.data = payload
        record = existing
    else:
        record = DevelopmentPlanRecord(
            project_id=project_id, mvp_version=approved.version, data=payload
        )
        session.add(record)

    await session.commit()
    await session.refresh(record)
    return record


async def get_latest_development_plan(
    session: AsyncSession, project_id: uuid.UUID
) -> DevelopmentPlanRecord | None:
    return await session.scalar(
        select(DevelopmentPlanRecord)
        .where(DevelopmentPlanRecord.project_id == project_id)
        .order_by(desc(DevelopmentPlanRecord.created_at))
        .limit(1)
    )


async def run_development_job(
    session: AsyncSession, project_id: uuid.UUID, job_id: uuid.UUID
) -> None:
    job = await session.get(ProcessingJob, job_id)
    if job is None:
        return
    job.status = JobStatus.RUNNING
    job.started_at = datetime.now(UTC)
    job.attempt_count += 1
    await session.commit()

    try:
        await generate_development_plan(session, project_id)
    except Exception as exc:  # noqa: BLE001 - captured to the job record
        job.status = JobStatus.FAILED
        job.error_message = str(exc)
        await session.commit()
        raise

    job.status = JobStatus.COMPLETED
    job.completed_at = datetime.now(UTC)
    await session.commit()
