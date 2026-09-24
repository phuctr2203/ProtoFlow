import uuid
from datetime import datetime
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession

from app.ai.schemas.mvp import MVPSpecification
from app.db.database import get_session
from app.db.models.mvp import MVPSpecificationRecord
from app.domain.mvp import service
from app.domain.mvp.service import NoIntelligenceError

router = APIRouter(tags=["mvp"])

SessionDep = Annotated[AsyncSession, Depends(get_session)]


class MVPResponse(BaseModel):
    version: int
    status: str
    created_at: datetime
    spec: MVPSpecification


class MVPVersionSummary(BaseModel):
    version: int
    status: str
    created_at: datetime


def _to_response(record: MVPSpecificationRecord) -> MVPResponse:
    return MVPResponse(
        version=record.version,
        status=record.status,
        created_at=record.created_at,
        spec=MVPSpecification.model_validate(record.data),
    )


@router.get("/projects/{project_id}/mvp", response_model=MVPResponse)
async def get_mvp(project_id: uuid.UUID, session: SessionDep) -> MVPResponse:
    record = await service.get_latest_mvp(session, project_id)
    if record is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "No MVP has been generated yet")
    return _to_response(record)


@router.post(
    "/projects/{project_id}/mvp", response_model=MVPResponse, status_code=status.HTTP_201_CREATED
)
async def create_mvp(project_id: uuid.UUID, session: SessionDep) -> MVPResponse:
    try:
        record = await service.generate_mvp(session, project_id)
    except NoIntelligenceError as exc:
        raise HTTPException(status.HTTP_409_CONFLICT, str(exc)) from None
    return _to_response(record)


@router.get("/projects/{project_id}/mvp/versions", response_model=list[MVPVersionSummary])
async def list_mvp_versions(project_id: uuid.UUID, session: SessionDep) -> list[MVPVersionSummary]:
    records = await service.list_mvps(session, project_id)
    return [
        MVPVersionSummary(version=r.version, status=r.status, created_at=r.created_at)
        for r in records
    ]
