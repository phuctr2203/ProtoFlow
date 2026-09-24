import uuid
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.database import get_session
from app.domain.projects import service
from app.domain.projects.schemas import ProjectCreate, ProjectRead

router = APIRouter(prefix="/projects", tags=["projects"])

SessionDep = Annotated[AsyncSession, Depends(get_session)]


@router.post("", response_model=ProjectRead, status_code=status.HTTP_201_CREATED)
async def create_project(data: ProjectCreate, session: SessionDep) -> ProjectRead:
    project = await service.create_project(session, data)
    return ProjectRead.model_validate(project)


@router.get("", response_model=list[ProjectRead])
async def list_projects(session: SessionDep) -> list[ProjectRead]:
    projects = await service.list_projects(session)
    return [ProjectRead.model_validate(p) for p in projects]


@router.get("/{project_id}", response_model=ProjectRead)
async def get_project(project_id: uuid.UUID, session: SessionDep) -> ProjectRead:
    try:
        project = await service.get_project(session, project_id)
    except service.ProjectNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Project not found"
        ) from None
    return ProjectRead.model_validate(project)
