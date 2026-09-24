import uuid

import pytest

from app.ai.schemas.intelligence import Extraction, RequirementStatus
from app.domain.intelligence import service as intel_service
from app.domain.meetings import service as meeting_service
from app.integrations.meetings.fixtures import PROFILES


async def _prepare_meeting(session_factory, project_id: str, fixture: str) -> uuid.UUID:
    async with session_factory() as session:
        meeting = await meeting_service.create_meeting(
            session,
            project_id=uuid.UUID(project_id),
            external_meeting_id=fixture,
            title=f"Meeting {fixture}",
        )
        meeting_id = meeting.id
    async with session_factory() as session:
        await meeting_service.process_transcript(session, meeting_id)
    return meeting_id


@pytest.mark.parametrize("fixture", PROFILES)
async def test_intelligence_produced_for_every_fixture(client, session_factory, fixture):
    project_id = (await client.post("/api/v1/projects", json={"name": "Acme"})).json()["id"]
    meeting_id = await _prepare_meeting(session_factory, project_id, fixture)

    async with session_factory() as session:
        intel = await intel_service.run_meeting_intelligence(session, meeting_id)

    assert len(intel.requirements) >= 1
    # Every requirement is either backed by evidence (CONFIRMED) or explicitly flagged.
    for req in intel.requirements:
        if req.status == RequirementStatus.CONFIRMED:
            assert req.extraction == Extraction.EXPLICIT
            assert req.source is not None and req.source.quote and req.source.speaker
        else:
            assert req.status == RequirementStatus.NEEDS_REVIEW

    # The inferred requirement is never presented as confirmed client scope.
    inferred = [r for r in intel.requirements if r.extraction == Extraction.INFERRED]
    assert all(r.status == RequirementStatus.NEEDS_REVIEW for r in inferred)


async def test_noisy_fixture_flags_needs_review(client, session_factory):
    project_id = (await client.post("/api/v1/projects", json={"name": "Acme"})).json()["id"]
    meeting_id = await _prepare_meeting(session_factory, project_id, "combined")

    async with session_factory() as session:
        intel = await intel_service.run_meeting_intelligence(session, meeting_id)

    # The combined-noise profile must not produce all-confident output.
    assert any(r.status == RequirementStatus.NEEDS_REVIEW for r in intel.requirements)

    resp = await client.get(f"/api/v1/meetings/{meeting_id}/intelligence")
    assert resp.status_code == 200
    assert len(resp.json()["requirements"]) >= 1


async def test_intelligence_404_before_run(client, session_factory):
    project_id = (await client.post("/api/v1/projects", json={"name": "Acme"})).json()["id"]
    meeting_id = await _prepare_meeting(session_factory, project_id, "clean")
    resp = await client.get(f"/api/v1/meetings/{meeting_id}/intelligence")
    assert resp.status_code == 404
