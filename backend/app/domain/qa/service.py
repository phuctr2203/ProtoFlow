import json
import uuid
from datetime import UTC, datetime

from sqlalchemy import desc, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.ai.graphs.qa import run_qa
from app.ai.llm.registry import get_dev_llm_provider
from app.ai.schemas.mvp import MVPSpecification, Scope
from app.ai.schemas.qa import FeatureCoverage, QAReport, TestCase, TestStatus
from app.db.models.processing import JobStatus, ProcessingJob
from app.db.models.qa import QAReportRecord
from app.domain.development import service as development_service
from app.domain.mvp.approval import require_approved_mvp


class CodeNotGeneratedError(Exception):
    """Raised when QA is attempted before code has been generated (Epic 7 ← Epic 6)."""


def build_report(mvp: MVPSpecification, tests: list[TestCase]) -> QAReport:
    coverage: list[FeatureCoverage] = []
    for feature in mvp.features:
        test_ids = [t.id for t in tests if t.feature == feature.name]
        coverage.append(
            FeatureCoverage(
                feature=feature.name,
                scope=feature.scope.value,
                covered=bool(test_ids),
                test_ids=test_ids,
            )
        )

    must_have = [c for c in coverage if c.scope == Scope.MUST_HAVE.value]
    must_have_covered = all(c.covered for c in must_have) if must_have else True

    passed = sum(1 for t in tests if t.status == TestStatus.PASS)
    failed = sum(1 for t in tests if t.status == TestStatus.FAIL)
    blocked = sum(1 for t in tests if t.status == TestStatus.BLOCKED)
    demo_ready = must_have_covered and failed == 0 and blocked == 0

    return QAReport(
        test_cases=tests,
        coverage=coverage,
        total=len(tests),
        passed=passed,
        failed=failed,
        blocked=blocked,
        must_have_covered=must_have_covered,
        demo_ready=demo_ready,
    )


async def generate_qa_report(session: AsyncSession, project_id: uuid.UUID) -> QAReportRecord:
    approved = await require_approved_mvp(session, project_id)
    code = await development_service.get_latest_code_generation(session, project_id)
    if code is None:
        raise CodeNotGeneratedError(
            f"Project {project_id} has no generated code yet; run code generation before QA."
        )

    test_list = await run_qa(
        mvp_text=json.dumps(approved.data, ensure_ascii=False),
        provider=get_dev_llm_provider(),
    )
    mvp = MVPSpecification.model_validate(approved.data)
    report = build_report(mvp, test_list.test_cases)

    existing = await session.scalar(
        select(QAReportRecord).where(
            QAReportRecord.project_id == project_id,
            QAReportRecord.mvp_version == approved.version,
        )
    )
    payload = report.model_dump(mode="json")
    if existing is not None:
        existing.data = payload
        existing.demo_ready = report.demo_ready
        record = existing
    else:
        record = QAReportRecord(
            project_id=project_id,
            mvp_version=approved.version,
            demo_ready=report.demo_ready,
            data=payload,
        )
        session.add(record)

    await session.commit()
    await session.refresh(record)
    return record


async def get_latest_qa_report(
    session: AsyncSession, project_id: uuid.UUID
) -> QAReportRecord | None:
    return await session.scalar(
        select(QAReportRecord)
        .where(QAReportRecord.project_id == project_id)
        .order_by(desc(QAReportRecord.created_at))
        .limit(1)
    )


async def run_qa_job(session: AsyncSession, project_id: uuid.UUID, job_id: uuid.UUID) -> None:
    job = await session.get(ProcessingJob, job_id)
    if job is None:
        return
    job.status = JobStatus.RUNNING
    job.started_at = datetime.now(UTC)
    job.attempt_count += 1
    await session.commit()

    try:
        await generate_qa_report(session, project_id)
    except Exception as exc:  # noqa: BLE001 - captured to the job record
        job.status = JobStatus.FAILED
        job.error_message = str(exc)
        await session.commit()
        raise

    job.status = JobStatus.COMPLETED
    job.completed_at = datetime.now(UTC)
    await session.commit()
