import uuid
from datetime import datetime
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession

from app.ai.schemas.demo import DemoPackage
from app.db.database import get_session
from app.domain.demo import service
from app.domain.demo.service import QANotReadyError
from app.domain.mvp.approval import MVPNotApprovedError

router = APIRouter(tags=["demo"])

SessionDep = Annotated[AsyncSession, Depends(get_session)]


class DemoResponse(BaseModel):
    mvp_version: int
    created_at: datetime
    demo: DemoPackage


@router.get("/projects/{project_id}/demo", response_model=DemoResponse)
async def get_demo(project_id: uuid.UUID, session: SessionDep) -> DemoResponse:
    record = await service.get_latest_demo(session, project_id)
    if record is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "No demo has been prepared yet")
    return DemoResponse(
        mvp_version=record.mvp_version,
        created_at=record.created_at,
        demo=DemoPackage.model_validate(record.data),
    )


@router.post(
    "/projects/{project_id}/demo",
    response_model=DemoResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_demo(project_id: uuid.UUID, session: SessionDep) -> DemoResponse:
    try:
        record = await service.generate_demo(session, project_id)
    except (MVPNotApprovedError, QANotReadyError) as exc:
        raise HTTPException(status.HTTP_409_CONFLICT, str(exc)) from None
    return DemoResponse(
        mvp_version=record.mvp_version,
        created_at=record.created_at,
        demo=DemoPackage.model_validate(record.data),
    )
