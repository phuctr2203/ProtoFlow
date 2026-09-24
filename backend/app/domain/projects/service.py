import uuid

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models.project import Project
from app.domain.projects.schemas import ProjectCreate


class ProjectNotFoundError(Exception):
    def __init__(self, project_id: uuid.UUID) -> None:
        super().__init__(f"Project {project_id} not found")
        self.project_id = project_id


async def create_project(session: AsyncSession, data: ProjectCreate) -> Project:
    project = Project(name=data.name, description=data.description)
    session.add(project)
    await session.commit()
    await session.refresh(project)
    return project


async def list_projects(session: AsyncSession) -> list[Project]:
    result = await session.execute(select(Project).order_by(Project.created_at.desc()))
    return list(result.scalars().all())


async def get_project(session: AsyncSession, project_id: uuid.UUID) -> Project:
    project = await session.get(Project, project_id)
    if project is None:
        raise ProjectNotFoundError(project_id)
    return project
