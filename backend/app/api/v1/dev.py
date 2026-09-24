import uuid
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.database import get_session
from app.domain.meetings import service
from app.domain.meetings.schemas import SimulateMeetingRequest
from app.integrations.meetings.fixtures import PROFILES
from app.workers.queue import get_queue

router = APIRouter(prefix="/dev", tags=["dev"])

SessionDep = Annotated[AsyncSession, Depends(get_session)]
QueueDep = Annotated[object, Depends(get_queue)]


@router.post("/simulate-meeting", status_code=status.HTTP_202_ACCEPTED)
async def simulate_meeting(data: SimulateMeetingRequest, session: SessionDep, queue: QueueDep):
    """Dev-only: create a completed meeting from a fixture and emit a transcript-ready
    event through the same path a real provider webhook would take (Idea.MD §62)."""
    if data.fixture not in PROFILES:
        raise HTTPException(
            status.HTTP_422_UNPROCESSABLE_CONTENT,
            f"Unknown fixture '{data.fixture}'. Available: {', '.join(PROFILES)}",
        )

    await service.create_meeting(
        session,
        project_id=data.project_id,
        external_meeting_id=data.fixture,
        title=data.title or f"Simulated meeting ({data.fixture})",
        provider="mock",
    )
    return await service.handle_transcript_ready(
        session,
        queue,
        provider="mock",
        external_event_id=str(uuid.uuid4()),
        external_meeting_id=data.fixture,
        payload={"fixture": data.fixture},
    )
