import uuid

from sqlalchemy import desc, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models.approval import ApprovalAction, MVPApproval
from app.db.models.mvp import MVPSpecificationRecord, MVPStatus
from app.db.models.project import Project, ProjectStatus

_ACTION_TO_STATUS = {
    ApprovalAction.APPROVE: MVPStatus.APPROVED,
    ApprovalAction.REJECT: MVPStatus.REJECTED,
    ApprovalAction.REQUEST_REVISION: MVPStatus.REVISION_REQUESTED,
}


class MVPVersionNotFoundError(Exception):
    pass


class MVPNotApprovedError(Exception):
    """Raised when a downstream phase is attempted without an approved MVP (FR-11)."""


async def decide(
    session: AsyncSession,
    *,
    project_id: uuid.UUID,
    version: int,
    action: ApprovalAction,
    approved_by: str,
    comments: str | None = None,
) -> MVPSpecificationRecord:
    record = await session.scalar(
        select(MVPSpecificationRecord).where(
            MVPSpecificationRecord.project_id == project_id,
            MVPSpecificationRecord.version == version,
        )
    )
    if record is None:
        raise MVPVersionNotFoundError(f"MVP v{version} not found for project {project_id}")

    record.status = _ACTION_TO_STATUS[action]
    session.add(
        MVPApproval(
            project_id=project_id,
            mvp_id=record.id,
            version=version,
            action=action,
            approved_by=approved_by,
            comments=comments,
        )
    )

    if action == ApprovalAction.APPROVE:
        project = await session.get(Project, project_id)
        if project is not None:
            project.status = ProjectStatus.DESIGN

    await session.commit()
    await session.refresh(record)
    return record


async def get_approved_mvp(
    session: AsyncSession, project_id: uuid.UUID
) -> MVPSpecificationRecord | None:
    return await session.scalar(
        select(MVPSpecificationRecord)
        .where(
            MVPSpecificationRecord.project_id == project_id,
            MVPSpecificationRecord.status == MVPStatus.APPROVED,
        )
        .order_by(desc(MVPSpecificationRecord.version))
        .limit(1)
    )


async def require_approved_mvp(
    session: AsyncSession, project_id: uuid.UUID
) -> MVPSpecificationRecord:
    record = await get_approved_mvp(session, project_id)
    if record is None:
        raise MVPNotApprovedError(
            f"Project {project_id} has no approved MVP; approval is required first."
        )
    return record
