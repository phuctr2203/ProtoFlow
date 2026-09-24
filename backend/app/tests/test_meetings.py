import uuid

import pytest
from httpx import AsyncClient
from sqlalchemy import func, select

from app.db.models.processing import MeetingEvent
from app.domain.meetings import service
from app.integrations.meetings.fixtures import PROFILES


async def _create_project(client: AsyncClient) -> str:
    resp = await client.post("/api/v1/projects", json={"name": "Acme Corp"})
    return resp.json()["id"]


@pytest.mark.parametrize("fixture", PROFILES)
async def test_simulate_drives_meeting_to_transcript_ready(client, session_factory, fixture):
    project_id = await _create_project(client)

    resp = await client.post(
        "/api/v1/dev/simulate-meeting",
        json={"project_id": project_id, "fixture": fixture},
    )
    assert resp.status_code == 202
    body = resp.json()
    assert body["status"] == "queued"

    # The worker isn't running under test — run the enqueued job directly.
    async with session_factory() as session:
        await service.run_transcript_job(
            session, uuid.UUID(body["meeting_id"]), uuid.UUID(body["job_id"])
        )

    meeting = await client.get(f"/api/v1/meetings/{body['meeting_id']}")
    assert meeting.json()["status"] == "TRANSCRIPT_READY"

    transcript = await client.get(f"/api/v1/meetings/{body['meeting_id']}/transcript")
    assert transcript.status_code == 200
    assert len(transcript.json()["segments"]) >= 1


async def test_webhook_is_idempotent(client, session_factory, fake_queue):
    project_id = await _create_project(client)
    async with session_factory() as session:
        await service.create_meeting(
            session,
            project_id=uuid.UUID(project_id),
            external_meeting_id="clean",
            title="Acme discovery call",
        )

    payload = {"external_event_id": "evt-123", "external_meeting_id": "clean"}
    first = await client.post("/api/v1/webhooks/mock", json=payload)
    second = await client.post("/api/v1/webhooks/mock", json=payload)

    assert first.json()["status"] == "queued"
    assert second.json()["status"] == "duplicate"

    # The job was enqueued exactly once.
    enqueued = [j for j in fake_queue.jobs if j[0] == "process_transcript"]
    assert len(enqueued) == 1

    # Exactly one event row exists for the idempotency key.
    async with session_factory() as session:
        count = await session.scalar(select(func.count()).select_from(MeetingEvent))
    assert count == 1


async def test_webhook_unknown_meeting_returns_404(client):
    resp = await client.post(
        "/api/v1/webhooks/mock",
        json={"external_event_id": "e1", "external_meeting_id": "clean"},
    )
    assert resp.status_code == 404


async def test_webhook_missing_fields_returns_422(client):
    resp = await client.post("/api/v1/webhooks/mock", json={"external_event_id": "e1"})
    assert resp.status_code == 422
