import json
import uuid
from datetime import UTC, datetime
from pathlib import Path

from sqlalchemy import desc, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.ai.engines.registry import get_coding_engine
from app.ai.graphs.development_plan import run_development_plan
from app.ai.llm.registry import get_dev_llm_provider
from app.ai.schemas.development import CodingResult, DevelopmentPlan
from app.core.config import settings
from app.db.models.development import CodeGenerationRecord, DevelopmentPlanRecord
from app.db.models.processing import JobStatus, ProcessingJob
from app.domain.design import service as design_service
from app.domain.development.inspection import inspect_repository
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


async def generate_code(session: AsyncSession, project_id: uuid.UUID) -> CodeGenerationRecord:
    """Implement the MVP from its development plan using the configured coding engine (FR-15).
    Reuses generate_development_plan, which enforces the approved-MVP (FR-11) and design gates."""
    plan_record = await generate_development_plan(session, project_id)
    plan = DevelopmentPlan.model_validate(plan_record.data)
    approved = await require_approved_mvp(session, project_id)

    workspace = Path(settings.workspace_root) / str(project_id)
    workspace.mkdir(parents=True, exist_ok=True)
    inspection = inspect_repository(workspace)

    engine = get_coding_engine()
    result: CodingResult = await engine.implement(
        workspace=str(workspace),
        plan=plan,
        inspection=inspection,
        mvp_text=json.dumps(approved.data, ensure_ascii=False),
    )

    existing = await session.scalar(
        select(CodeGenerationRecord).where(
            CodeGenerationRecord.project_id == project_id,
            CodeGenerationRecord.mvp_version == approved.version,
        )
    )
    payload = result.model_dump(mode="json")
    if existing is not None:
        existing.data = payload
        existing.engine = engine.name
        record = existing
    else:
        record = CodeGenerationRecord(
            project_id=project_id,
            mvp_version=approved.version,
            engine=engine.name,
            data=payload,
        )
        session.add(record)

    await session.commit()
    await session.refresh(record)
    return record


async def get_latest_code_generation(
    session: AsyncSession, project_id: uuid.UUID
) -> CodeGenerationRecord | None:
    return await session.scalar(
        select(CodeGenerationRecord)
        .where(CodeGenerationRecord.project_id == project_id)
        .order_by(desc(CodeGenerationRecord.created_at))
        .limit(1)
    )


async def run_code_generation_job(
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
        await generate_code(session, project_id)
    except Exception as exc:  # noqa: BLE001 - captured to the job record
        job.status = JobStatus.FAILED
        job.error_message = str(exc)
        await session.commit()
        raise

    job.status = JobStatus.COMPLETED
    job.completed_at = datetime.now(UTC)
    await session.commit()
