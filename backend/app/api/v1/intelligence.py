import uuid
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.ai.schemas.intelligence import MeetingIntelligence
from app.db.database import get_session
from app.domain.intelligence import service

router = APIRouter(tags=["intelligence"])

SessionDep = Annotated[AsyncSession, Depends(get_session)]


@router.get("/meetings/{meeting_id}/intelligence", response_model=MeetingIntelligence)
async def get_meeting_intelligence(
    meeting_id: uuid.UUID, session: SessionDep
) -> MeetingIntelligence:
    record = await service.get_intelligence(session, meeting_id)
    if record is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Intelligence not available yet")
    return MeetingIntelligence.model_validate(record.data)
