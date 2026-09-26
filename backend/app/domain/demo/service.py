import json
import uuid
from datetime import UTC, datetime

from sqlalchemy import desc, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.ai.graphs.demo import run_demo
from app.ai.llm.registry import get_dev_llm_provider
from app.ai.schemas.demo import Capability, CapabilityStatus, DemoPackage
from app.ai.schemas.mvp import MVPSpecification, Scope
from app.ai.schemas.qa import QAReport
from app.db.models.demo import DemoRecord
from app.db.models.processing import JobStatus, ProcessingJob
from app.domain.mvp.approval import require_approved_mvp
from app.domain.qa import service as qa_service


class QANotReadyError(Exception):
    """Raised when demo prep is attempted before a QA report exists (Epic 8 ← Epic 7)."""


def derive_capabilities(mvp: MVPSpecification, qa: QAReport) -> list[Capability]:
    """Honest labeling (FR-19): a feature is IMPLEMENTED only if QA covers it; in-scope but
    uncovered features are SIMULATED; out-of-scope items are NOT_IMPLEMENTED."""
    covered = {c.feature for c in qa.coverage if c.covered}
    capabilities: list[Capability] = []
    for feature in mvp.features:
        if feature.scope == Scope.OUT_OF_SCOPE:
            status = CapabilityStatus.NOT_IMPLEMENTED
        elif feature.name in covered:
            status = CapabilityStatus.IMPLEMENTED
        else:
            status = CapabilityStatus.SIMULATED
        capabilities.append(Capability(name=feature.name, status=status, note=feature.scope.value))
    for item in mvp.out_of_scope:
        capabilities.append(
            Capability(name=item, status=CapabilityStatus.NOT_IMPLEMENTED, note="Out of scope")
        )
    return capabilities


async def generate_demo(session: AsyncSession, project_id: uuid.UUID) -> DemoRecord:
    approved = await require_approved_mvp(session, project_id)
    qa_record = await qa_service.get_latest_qa_report(session, project_id)
    if qa_record is None:
        raise QANotReadyError(
            f"Project {project_id} has no QA report yet; run QA before preparing a demo."
        )

    mvp = MVPSpecification.model_validate(approved.data)
    qa = QAReport.model_validate(qa_record.data)

    narrative = await run_demo(
        context=json.dumps(approved.data, ensure_ascii=False),
        provider=get_dev_llm_provider(),
    )
    package = DemoPackage(
        **narrative.model_dump(),
        capabilities=derive_capabilities(mvp, qa),
    )

    existing = await session.scalar(
        select(DemoRecord).where(
            DemoRecord.project_id == project_id,
            DemoRecord.mvp_version == approved.version,
        )
    )
    payload = package.model_dump(mode="json")
    if existing is not None:
        existing.data = payload
        record = existing
    else:
        record = DemoRecord(project_id=project_id, mvp_version=approved.version, data=payload)
        session.add(record)

    await session.commit()
    await session.refresh(record)
    return record


async def get_latest_demo(session: AsyncSession, project_id: uuid.UUID) -> DemoRecord | None:
    return await session.scalar(
        select(DemoRecord)
        .where(DemoRecord.project_id == project_id)
        .order_by(desc(DemoRecord.created_at))
        .limit(1)
    )


async def run_demo_job(session: AsyncSession, project_id: uuid.UUID, job_id: uuid.UUID) -> None:
    job = await session.get(ProcessingJob, job_id)
    if job is None:
        return
    job.status = JobStatus.RUNNING
    job.started_at = datetime.now(UTC)
    job.attempt_count += 1
    await session.commit()

    try:
        await generate_demo(session, project_id)
    except Exception as exc:  # noqa: BLE001 - captured to the job record
        job.status = JobStatus.FAILED
        job.error_message = str(exc)
        await session.commit()
        raise

    job.status = JobStatus.COMPLETED
    job.completed_at = datetime.now(UTC)
    await session.commit()
