import uuid

import pytest

from app.core.config import settings
from app.db.models.approval import ApprovalAction
from app.domain.demo import service as demo_service
from app.domain.demo.service import QANotReadyError
from app.domain.design import service as design_service
from app.domain.development import service as development_service
from app.domain.intelligence import service as intel_service
from app.domain.meetings import service as meeting_service
from app.domain.mvp import approval
from app.domain.mvp import service as mvp_service
from app.domain.qa import service as qa_service


@pytest.fixture(autouse=True)
def _workspace(tmp_path, monkeypatch):
    monkeypatch.setattr(settings, "workspace_root", str(tmp_path / "ws"))
    monkeypatch.setattr(settings, "coding_engine", "mock")


async def _qa_ready_project(client, session_factory) -> str:
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
    async with session_factory() as session:
        await development_service.generate_code(session, uuid.UUID(project_id))
    async with session_factory() as session:
        await qa_service.generate_qa_report(session, uuid.UUID(project_id))
    return project_id


async def test_demo_blocked_without_qa(client, session_factory):
    project_id = (await client.post("/api/v1/projects", json={"name": "Empty"})).json()["id"]
    async with session_factory() as session:
        with pytest.raises(Exception):  # noqa: B017 - MVPNotApproved or QANotReady
            await demo_service.generate_demo(session, uuid.UUID(project_id))

    resp = await client.post(f"/api/v1/projects/{project_id}/demo")
    assert resp.status_code == 409


async def test_demo_labels_are_honest(client, session_factory):
    project_id = await _qa_ready_project(client, session_factory)

    resp = await client.post(f"/api/v1/projects/{project_id}/demo")
    assert resp.status_code == 201
    demo = resp.json()["demo"]

    assert demo["objective"]
    assert demo["script"]
    # Synthetic data is clearly marked (FR-18).
    assert all("SYNTHETIC" in d for d in demo["synthetic_data"])
    statuses = {c["status"] for c in demo["capabilities"]}
    assert "IMPLEMENTED" in statuses  # MUST_HAVE features covered by QA
    assert "NOT_IMPLEMENTED" in statuses  # out-of-scope items

    latest = await client.get(f"/api/v1/projects/{project_id}/demo")
    assert latest.status_code == 200
    assert latest.json()["mvp_version"] == 1


async def test_demo_qa_not_ready_error_directly(client, session_factory):
    # Approved MVP but no QA report -> QANotReadyError.
    project_id = (await client.post("/api/v1/projects", json={"name": "NoQA"})).json()["id"]
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
        with pytest.raises(QANotReadyError):
            await demo_service.generate_demo(session, uuid.UUID(project_id))
