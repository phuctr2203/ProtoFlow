import uuid

import pytest

from app.db.models.approval import ApprovalAction
from app.domain.design import service as design_service
from app.domain.intelligence import service as intel_service
from app.domain.meetings import service as meeting_service
from app.domain.mvp import approval
from app.domain.mvp import service as mvp_service
from app.domain.mvp.approval import MVPNotApprovedError


async def _project_with_approved_mvp(client, session_factory, *, approve: bool) -> str:
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
    if approve:
        async with session_factory() as session:
            await approval.decide(
                session,
                project_id=uuid.UUID(project_id),
                version=1,
                action=ApprovalAction.APPROVE,
                approved_by="consultant",
            )
    return project_id


async def test_design_blocked_without_approved_mvp(client, session_factory):
    project_id = await _project_with_approved_mvp(client, session_factory, approve=False)
    async with session_factory() as session:
        with pytest.raises(MVPNotApprovedError):
            await design_service.generate_design(session, uuid.UUID(project_id))

    resp = await client.post(f"/api/v1/projects/{project_id}/design")
    assert resp.status_code == 409


async def test_design_generated_from_approved_mvp(client, session_factory):
    project_id = await _project_with_approved_mvp(client, session_factory, approve=True)

    resp = await client.post(f"/api/v1/projects/{project_id}/design")
    assert resp.status_code == 201
    design = resp.json()["design"]
    assert design["screens"]
    assert design["apis"]
    assert design["tech_decisions"]

    latest = await client.get(f"/api/v1/projects/{project_id}/design")
    assert latest.status_code == 200
    assert latest.json()["mvp_version"] == 1
