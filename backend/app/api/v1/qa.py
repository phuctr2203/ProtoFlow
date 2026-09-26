import uuid
from datetime import datetime
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession

from app.ai.schemas.qa import QAReport
from app.db.database import get_session
from app.domain.mvp.approval import MVPNotApprovedError
from app.domain.qa import service
from app.domain.qa.service import CodeNotGeneratedError

router = APIRouter(tags=["qa"])

SessionDep = Annotated[AsyncSession, Depends(get_session)]


class QAReportResponse(BaseModel):
    mvp_version: int
    created_at: datetime
    demo_ready: bool
    report: QAReport


@router.get("/projects/{project_id}/qa", response_model=QAReportResponse)
async def get_qa_report(project_id: uuid.UUID, session: SessionDep) -> QAReportResponse:
    record = await service.get_latest_qa_report(session, project_id)
    if record is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "No QA report has been generated yet")
    return QAReportResponse(
        mvp_version=record.mvp_version,
        created_at=record.created_at,
        demo_ready=record.demo_ready,
        report=QAReport.model_validate(record.data),
    )


@router.post(
    "/projects/{project_id}/qa",
    response_model=QAReportResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_qa_report(project_id: uuid.UUID, session: SessionDep) -> QAReportResponse:
    try:
        record = await service.generate_qa_report(session, project_id)
    except (MVPNotApprovedError, CodeNotGeneratedError) as exc:
        raise HTTPException(status.HTTP_409_CONFLICT, str(exc)) from None
    return QAReportResponse(
        mvp_version=record.mvp_version,
        created_at=record.created_at,
        demo_ready=record.demo_ready,
        report=QAReport.model_validate(record.data),
    )
