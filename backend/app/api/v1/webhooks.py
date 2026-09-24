from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Request, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.database import get_session
from app.domain.meetings import service
from app.integrations.meetings.registry import get_provider
from app.workers.queue import get_queue

router = APIRouter(tags=["webhooks"])

SessionDep = Annotated[AsyncSession, Depends(get_session)]
QueueDep = Annotated[object, Depends(get_queue)]


@router.post("/webhooks/{provider}")
async def receive_webhook(provider: str, request: Request, session: SessionDep, queue: QueueDep):
    """Provider-agnostic transcript-ready webhook. Validates, persists the event
    idempotently, enqueues a job, and returns fast (Idea.MD §49, §72)."""
    try:
        prov = get_provider(provider)
    except KeyError:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Unknown provider") from None

    body = await request.body()
    if not await prov.verify_webhook(dict(request.headers), body):
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Invalid webhook signature")

    payload = await request.json()
    external_event_id = payload.get("external_event_id")
    external_meeting_id = payload.get("external_meeting_id")
    if not external_event_id or not external_meeting_id:
        raise HTTPException(
            status.HTTP_422_UNPROCESSABLE_CONTENT,
            "Missing external_event_id or external_meeting_id",
        )

    try:
        return await service.handle_transcript_ready(
            session,
            queue,
            provider=provider,
            external_event_id=external_event_id,
            external_meeting_id=external_meeting_id,
            event_type=payload.get("event_type", "transcript.ready"),
            payload=payload,
        )
    except service.MeetingNotFoundError:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Meeting not found") from None
