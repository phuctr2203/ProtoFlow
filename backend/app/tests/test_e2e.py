"""End-to-end walkthrough (Epic 9, Story 9.2, validates SM-1): one simulated meeting flows through
the entire pipeline — meeting → intelligence → MVP → approval → design → code → QA → demo — with no
manual data-fixing along the way."""

import uuid

import pytest

from app.core.config import settings
from app.db.models.approval import ApprovalAction
from app.domain.demo import service as demo_service
from app.domain.design import service as design_service
from app.domain.development import service as development_service
from app.domain.intelligence import service as intel_service
from app.domain.meetings import service as meeting_service
from app.domain.mvp import approval
from app.domain.mvp import service as mvp_service
from app.domain.projects.overview import get_project_overview
from app.domain.qa import service as qa_service


@pytest.fixture(autouse=True)
def _workspace(tmp_path, monkeypatch):
    monkeypatch.setattr(settings, "workspace_root", str(tmp_path / "ws"))
    monkeypatch.setattr(settings, "coding_engine", "mock")


async def test_full_pipeline_runs_end_to_end(client, session_factory):
    # 1. Project + simulated meeting
    project_id = (await client.post("/api/v1/projects", json={"name": "Acme"})).json()["id"]
    pid = uuid.UUID(project_id)
    async with session_factory() as session:
        meeting = await meeting_service.create_meeting(
            session, project_id=pid, external_meeting_id="clean", title="Discovery"
        )
        meeting_id = meeting.id

    # 2. Transcript -> 3. Intelligence
    async with session_factory() as session:
        await meeting_service.process_transcript(session, meeting_id)
    async with session_factory() as session:
        intel = await intel_service.run_meeting_intelligence(session, meeting_id)
    assert intel.requirements

    # 4. MVP -> 5. Human approval
    async with session_factory() as session:
        await mvp_service.generate_mvp(session, pid)
    async with session_factory() as session:
        await approval.decide(
            session,
            project_id=pid,
            version=1,
            action=ApprovalAction.APPROVE,
            approved_by="consultant",
        )

    # 6. Design -> 7. Code (PR) -> 8. QA -> 9. Demo
    async with session_factory() as session:
        design = await design_service.generate_design(session, pid)
    assert design.data["screens"]
    async with session_factory() as session:
        code = await development_service.generate_code(session, pid)
    assert code.data["pull_request_url"]
    async with session_factory() as session:
        qa = await qa_service.generate_qa_report(session, pid)
    assert qa.demo_ready is True
    async with session_factory() as session:
        demo = await demo_service.generate_demo(session, pid)
    assert demo.data["capabilities"]

    # Cross-phase overview reflects the real state (FR-20): every phase complete.
    async with session_factory() as session:
        overview = await get_project_overview(session, pid)
    by_phase = {p.phase: p.status for p in overview.phases}
    assert by_phase["Meeting"] == "complete"
    assert by_phase["Intelligence"] == "complete"
    assert by_phase["MVP"] == "complete"
    assert by_phase["Design"] == "complete"
    assert by_phase["Development"] == "complete"
    assert by_phase["QA"] == "complete"
    assert by_phase["Demo"] == "complete"


async def test_overview_via_api_before_any_work(client):
    project_id = (await client.post("/api/v1/projects", json={"name": "Fresh"})).json()["id"]
    resp = await client.get(f"/api/v1/projects/{project_id}/overview")
    assert resp.status_code == 200
    statuses = {p["phase"]: p["status"] for p in resp.json()["phases"]}
    assert statuses["Meeting"] == "pending"
    assert statuses["Demo"] == "pending"
