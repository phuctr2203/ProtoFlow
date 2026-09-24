import uuid
from datetime import datetime
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession

from app.ai.schemas.design import DesignSpec
from app.db.database import get_session
from app.domain.design import service
from app.domain.mvp.approval import MVPNotApprovedError

router = APIRouter(tags=["design"])

SessionDep = Annotated[AsyncSession, Depends(get_session)]


class DesignResponse(BaseModel):
    mvp_version: int
    created_at: datetime
    design: DesignSpec


@router.get("/projects/{project_id}/design", response_model=DesignResponse)
async def get_design(project_id: uuid.UUID, session: SessionDep) -> DesignResponse:
    record = await service.get_latest_design(session, project_id)
    if record is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "No design has been generated yet")
    return DesignResponse(
        mvp_version=record.mvp_version,
        created_at=record.created_at,
        design=DesignSpec.model_validate(record.data),
    )


@router.post(
    "/projects/{project_id}/design",
    response_model=DesignResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_design(project_id: uuid.UUID, session: SessionDep) -> DesignResponse:
    try:
        record = await service.generate_design(session, project_id)
    except MVPNotApprovedError as exc:
        raise HTTPException(status.HTTP_409_CONFLICT, str(exc)) from None
    return DesignResponse(
        mvp_version=record.mvp_version,
        created_at=record.created_at,
        design=DesignSpec.model_validate(record.data),
    )
