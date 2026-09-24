import uuid
from pathlib import Path

import pytest

from app.ai.engines.registry import get_coding_engine
from app.core.config import settings
from app.db.models.approval import ApprovalAction
from app.domain.design import service as design_service
from app.domain.development import service as development_service
from app.domain.intelligence import service as intel_service
from app.domain.meetings import service as meeting_service
from app.domain.mvp import approval
from app.domain.mvp import service as mvp_service
from app.domain.mvp.approval import MVPNotApprovedError


@pytest.fixture(autouse=True)
def _workspace(tmp_path, monkeypatch):
    monkeypatch.setattr(settings, "workspace_root", str(tmp_path / "ws"))
    monkeypatch.setattr(settings, "coding_engine", "mock")


async def _designed_project(client, session_factory) -> str:
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
    async with session_factory() as session:
        await approval.decide(
            session,
            project_id=uuid.UUID(project_id),
            version=1,
            action=ApprovalAction.APPROVE,
            approved_by="consultant",
        )
    async with session_factory() as session:
        await design_service.generate_design(session, uuid.UUID(project_id))
    return project_id


def test_mock_engine_is_default():
    assert get_coding_engine().name == "mock"


async def test_code_generation_blocked_without_approved_mvp(client, session_factory):
    project_id = (await client.post("/api/v1/projects", json={"name": "Empty"})).json()["id"]
    async with session_factory() as session:
        with pytest.raises(MVPNotApprovedError):
            await development_service.generate_code(session, uuid.UUID(project_id))

    resp = await client.post(f"/api/v1/projects/{project_id}/code")
    assert resp.status_code == 409


async def test_code_generation_writes_workspace_and_persists(client, session_factory):
    project_id = await _designed_project(client, session_factory)

    resp = await client.post(f"/api/v1/projects/{project_id}/code")
    assert resp.status_code == 201
    body = resp.json()
    assert body["engine"] == "mock"
    assert body["result"]["files_changed"]
    assert body["result"]["branch"]

    # Files were actually materialized in the workspace.
    workspace = Path(settings.workspace_root) / project_id
    assert (workspace / "GENERATED_PLAN.md").exists()

    latest = await client.get(f"/api/v1/projects/{project_id}/code")
    assert latest.status_code == 200
    assert latest.json()["mvp_version"] == 1
