import uuid

import pytest

from app.db.models.approval import ApprovalAction
from app.domain.intelligence import service as intel_service
from app.domain.meetings import service as meeting_service
from app.domain.mvp import approval
from app.domain.mvp import service as mvp_service


async def _project_with_mvp(client, session_factory) -> str:
    project_id = (await client.post("/api/v1/projects", json={"name": "Acme"})).json()["id"]
    async with session_factory() as session:
        meeting = await meeting_service.create_meeting(
            session, project_id=uuid.UUID(project_id), external_meeting_id="clean", title="D"
        )
        meeting_id = meeting.id
    async with session_factory() as session:
        await meeting_service.process_transcript(session, meeting_id)
    async with session_factory() as session:
        await intel_service.run_meeting_intelligence(session, meeting_id)
    async with session_factory() as session:
        await mvp_service.generate_mvp(session, uuid.UUID(project_id))
    return project_id


async def test_approve_sets_status_and_persists(client, session_factory):
    project_id = await _project_with_mvp(client, session_factory)

    resp = await client.post(
        f"/api/v1/projects/{project_id}/mvp/approve",
        json={"version": 1, "action": "APPROVE", "approved_by": "consultant"},
    )
    assert resp.status_code == 200
    assert resp.json()["status"] == "APPROVED"

    async with session_factory() as session:
        approved = await approval.require_approved_mvp(session, uuid.UUID(project_id))
    assert approved.version == 1


async def test_reject_sets_status(client, session_factory):
    project_id = await _project_with_mvp(client, session_factory)
    resp = await client.post(
        f"/api/v1/projects/{project_id}/mvp/approve",
        json={"version": 1, "action": "REJECT", "approved_by": "consultant", "comments": "too big"},
    )
    assert resp.json()["status"] == "REJECTED"


async def test_require_approved_raises_without_approval(client, session_factory):
    project_id = await _project_with_mvp(client, session_factory)
    async with session_factory() as session:
        with pytest.raises(approval.MVPNotApprovedError):
            await approval.require_approved_mvp(session, uuid.UUID(project_id))


async def test_approve_unknown_version_404(client, session_factory):
    project_id = await _project_with_mvp(client, session_factory)
    resp = await client.post(
        f"/api/v1/projects/{project_id}/mvp/approve",
        json={"version": 99, "action": "APPROVE", "approved_by": "consultant"},
    )
    assert resp.status_code == 404


def test_action_maps_to_status_covers_all_actions():
    assert set(approval._ACTION_TO_STATUS.keys()) == set(ApprovalAction)
