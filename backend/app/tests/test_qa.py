import uuid

import pytest

from app.core.config import settings
from app.db.models.approval import ApprovalAction
from app.domain.design import service as design_service
from app.domain.development import service as development_service
from app.domain.intelligence import service as intel_service
from app.domain.meetings import service as meeting_service
from app.domain.mvp import approval
from app.domain.mvp import service as mvp_service
from app.domain.qa import service as qa_service
from app.domain.qa.service import CodeNotGeneratedError


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


async def test_qa_blocked_without_generated_code(client, session_factory):
    project_id = await _designed_project(client, session_factory)
    async with session_factory() as session:
        with pytest.raises(CodeNotGeneratedError):
            await qa_service.generate_qa_report(session, uuid.UUID(project_id))

    resp = await client.post(f"/api/v1/projects/{project_id}/qa")
    assert resp.status_code == 409


async def test_qa_report_covers_must_haves_and_is_demo_ready(client, session_factory):
    project_id = await _designed_project(client, session_factory)
    async with session_factory() as session:
        await development_service.generate_code(session, uuid.UUID(project_id))

    resp = await client.post(f"/api/v1/projects/{project_id}/qa")
    assert resp.status_code == 201
    body = resp.json()
    report = body["report"]

    assert report["total"] == 5
    assert report["passed"] == 5
    assert report["failed"] == 0
    # Every MUST_HAVE feature is covered by >= 1 test (FR-17).
    assert report["must_have_covered"] is True
    assert body["demo_ready"] is True
    must_haves = [c for c in report["coverage"] if c["scope"] == "MUST_HAVE"]
    assert must_haves and all(c["covered"] for c in must_haves)

    latest = await client.get(f"/api/v1/projects/{project_id}/qa")
    assert latest.status_code == 200
    assert latest.json()["mvp_version"] == 1
