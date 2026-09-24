import uuid
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.database import get_session
from app.db.models.approval import ApprovalAction
from app.domain.mvp import approval
from app.domain.mvp.approval import MVPVersionNotFoundError
from app.workers.queue import get_queue

router = APIRouter(tags=["mvp"])

SessionDep = Annotated[AsyncSession, Depends(get_session)]
QueueDep = Annotated[object, Depends(get_queue)]


class ApprovalRequest(BaseModel):
    version: int
    action: ApprovalAction
    approved_by: str
    comments: str | None = None


class ApprovalResponse(BaseModel):
    version: int
    status: str


@router.post("/projects/{project_id}/mvp/approve", response_model=ApprovalResponse)
async def decide_mvp(
    project_id: uuid.UUID, data: ApprovalRequest, session: SessionDep, queue: QueueDep
) -> ApprovalResponse:
    try:
        record = await approval.decide(
            session,
            project_id=project_id,
            version=data.version,
            action=data.action,
            approved_by=data.approved_by,
            comments=data.comments,
        )
    except MVPVersionNotFoundError as exc:
        raise HTTPException(status.HTTP_404_NOT_FOUND, str(exc)) from None

    # On approval, kick off design generation automatically (Idea.MD §66/§70).
    if data.action == ApprovalAction.APPROVE:
        await queue.enqueue_job("process_design", str(project_id))

    return ApprovalResponse(version=record.version, status=record.status)
