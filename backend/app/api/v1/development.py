import uuid
from datetime import datetime
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession

from app.ai.schemas.development import CodingResult, DevelopmentPlan
from app.db.database import get_session
from app.domain.development import service
from app.domain.development.service import DesignNotReadyError
from app.domain.mvp.approval import MVPNotApprovedError

router = APIRouter(tags=["development"])

SessionDep = Annotated[AsyncSession, Depends(get_session)]


class DevelopmentPlanResponse(BaseModel):
    mvp_version: int
    created_at: datetime
    plan: DevelopmentPlan


class CodeGenerationResponse(BaseModel):
    mvp_version: int
    created_at: datetime
    engine: str
    result: CodingResult


@router.get("/projects/{project_id}/development", response_model=DevelopmentPlanResponse)
async def get_development_plan(
    project_id: uuid.UUID, session: SessionDep
) -> DevelopmentPlanResponse:
    record = await service.get_latest_development_plan(session, project_id)
    if record is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "No development plan has been generated yet")
    return DevelopmentPlanResponse(
        mvp_version=record.mvp_version,
        created_at=record.created_at,
        plan=DevelopmentPlan.model_validate(record.data),
    )


@router.post(
    "/projects/{project_id}/development",
    response_model=DevelopmentPlanResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_development_plan(
    project_id: uuid.UUID, session: SessionDep
) -> DevelopmentPlanResponse:
    try:
        record = await service.generate_development_plan(session, project_id)
    except (MVPNotApprovedError, DesignNotReadyError) as exc:
        raise HTTPException(status.HTTP_409_CONFLICT, str(exc)) from None
    return DevelopmentPlanResponse(
        mvp_version=record.mvp_version,
        created_at=record.created_at,
        plan=DevelopmentPlan.model_validate(record.data),
    )


@router.get("/projects/{project_id}/code", response_model=CodeGenerationResponse)
async def get_code_generation(project_id: uuid.UUID, session: SessionDep) -> CodeGenerationResponse:
    record = await service.get_latest_code_generation(session, project_id)
    if record is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "No code has been generated yet")
    return CodeGenerationResponse(
        mvp_version=record.mvp_version,
        created_at=record.created_at,
        engine=record.engine,
        result=CodingResult.model_validate(record.data),
    )


@router.post(
    "/projects/{project_id}/code",
    response_model=CodeGenerationResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_code_generation(
    project_id: uuid.UUID, session: SessionDep
) -> CodeGenerationResponse:
    try:
        record = await service.generate_code(session, project_id)
    except (MVPNotApprovedError, DesignNotReadyError) as exc:
        raise HTTPException(status.HTTP_409_CONFLICT, str(exc)) from None
    return CodeGenerationResponse(
        mvp_version=record.mvp_version,
        created_at=record.created_at,
        engine=record.engine,
        result=CodingResult.model_validate(record.data),
    )
