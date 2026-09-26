import uuid

from pydantic import BaseModel, Field
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models.intelligence import MeetingIntelligenceRecord
from app.db.models.meeting import Meeting
from app.db.models.mvp import MVPStatus
from app.domain.demo import service as demo_service
from app.domain.design import service as design_service
from app.domain.development import service as development_service
from app.domain.mvp import service as mvp_service
from app.domain.qa import service as qa_service


class PhaseStatus(BaseModel):
    phase: str
    status: str  # "complete" | "pending" | "awaiting_approval"
    detail: str = ""


class ProjectOverview(BaseModel):
    project_id: str
    phases: list[PhaseStatus] = Field(default_factory=list)


def _phase(name: str, complete: bool, detail: str = "") -> PhaseStatus:
    return PhaseStatus(phase=name, status="complete" if complete else "pending", detail=detail)


async def get_project_overview(session: AsyncSession, project_id: uuid.UUID) -> ProjectOverview:
    """Cross-phase status for a project (FR-20). Each phase reflects the real records produced by
    Epics 1-8 — no mock state."""
    phases: list[PhaseStatus] = []

    meeting_id = await session.scalar(
        select(Meeting.id).where(Meeting.project_id == project_id).limit(1)
    )
    phases.append(_phase("Meeting", meeting_id is not None))

    intel_id = await session.scalar(
        select(MeetingIntelligenceRecord.id)
        .join(Meeting, MeetingIntelligenceRecord.meeting_id == Meeting.id)
        .where(Meeting.project_id == project_id)
        .limit(1)
    )
    phases.append(_phase("Intelligence", intel_id is not None))

    mvp = await mvp_service.get_latest_mvp(session, project_id)
    if mvp is None:
        phases.append(PhaseStatus(phase="MVP", status="pending"))
    elif mvp.status == MVPStatus.APPROVED:
        phases.append(
            PhaseStatus(phase="MVP", status="complete", detail=f"v{mvp.version} approved")
        )
    else:
        phases.append(PhaseStatus(phase="MVP", status="awaiting_approval", detail=mvp.status.value))

    design = await design_service.get_latest_design(session, project_id)
    phases.append(_phase("Design", design is not None))

    code = await development_service.get_latest_code_generation(session, project_id)
    phases.append(_phase("Development", code is not None))

    qa = await qa_service.get_latest_qa_report(session, project_id)
    phases.append(_phase("QA", qa is not None, "demo-ready" if (qa and qa.demo_ready) else ""))

    demo = await demo_service.get_latest_demo(session, project_id)
    phases.append(_phase("Demo", demo is not None))

    return ProjectOverview(project_id=str(project_id), phases=phases)
