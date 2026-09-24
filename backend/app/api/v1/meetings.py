import uuid
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.db.database import get_session
from app.db.models.meeting import Meeting, Transcript
from app.domain.meetings import service
from app.domain.meetings.schemas import MeetingRead, TranscriptRead

router = APIRouter(tags=["meetings"])

SessionDep = Annotated[AsyncSession, Depends(get_session)]


@router.get("/projects/{project_id}/meetings", response_model=list[MeetingRead])
async def list_project_meetings(project_id: uuid.UUID, session: SessionDep) -> list[MeetingRead]:
    meetings = await service.list_meetings(session, project_id=project_id)
    return [MeetingRead.model_validate(m) for m in meetings]


@router.get("/meetings/{meeting_id}", response_model=MeetingRead)
async def get_meeting(meeting_id: uuid.UUID, session: SessionDep) -> MeetingRead:
    meeting = await session.get(Meeting, meeting_id)
    if meeting is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Meeting not found")
    return MeetingRead.model_validate(meeting)


@router.get("/meetings/{meeting_id}/transcript", response_model=TranscriptRead)
async def get_meeting_transcript(meeting_id: uuid.UUID, session: SessionDep) -> TranscriptRead:
    transcript = await session.scalar(
        select(Transcript)
        .where(Transcript.meeting_id == meeting_id)
        .options(selectinload(Transcript.segments))
    )
    if transcript is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Transcript not available")
    return TranscriptRead.model_validate(transcript)
