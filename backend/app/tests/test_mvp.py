import uuid

from app.ai.schemas.mvp import Scope
from app.domain.intelligence import service as intel_service
from app.domain.meetings import service as meeting_service
from app.domain.mvp import service as mvp_service


async def _project_with_intelligence(client, session_factory) -> str:
    project_id = (await client.post("/api/v1/projects", json={"name": "Acme"})).json()["id"]
    async with session_factory() as session:
        meeting = await meeting_service.create_meeting(
            session,
            project_id=uuid.UUID(project_id),
            external_meeting_id="clean",
            title="Discovery",
        )
        meeting_id = meeting.id
    async with session_factory() as session:
        await meeting_service.process_transcript(session, meeting_id)
    async with session_factory() as session:
        await intel_service.run_meeting_intelligence(session, meeting_id)
    return project_id


async def test_generate_mvp_stays_small(client, session_factory):
    project_id = await _project_with_intelligence(client, session_factory)

    async with session_factory() as session:
        record = await mvp_service.generate_mvp(session, uuid.UUID(project_id))

    assert record.version == 1
    spec = record.data
    # Every feature carries a scope classification.
    scopes = {f["scope"] for f in spec["features"]}
    assert scopes.issubset({s.value for s in Scope})
    # The kept feature set is small and demoable, not the full product.
    assert len(spec["features"]) <= 8
    assert any(f["scope"] == Scope.MUST_HAVE.value for f in spec["features"])
    assert spec["out_of_scope"]  # non-essentials explicitly excluded
    assert spec["demo_scenario"]


async def test_mvp_versioning_never_overwrites(client, session_factory):
    project_id = await _project_with_intelligence(client, session_factory)
    async with session_factory() as session:
        v1 = await mvp_service.generate_mvp(session, uuid.UUID(project_id))
    async with session_factory() as session:
        v2 = await mvp_service.generate_mvp(session, uuid.UUID(project_id))
    assert v1.version == 1
    assert v2.version == 2

    versions = await client.get(f"/api/v1/projects/{project_id}/mvp/versions")
    assert len(versions.json()) == 2


async def test_mvp_api_generate_and_get(client, session_factory):
    project_id = await _project_with_intelligence(client, session_factory)

    created = await client.post(f"/api/v1/projects/{project_id}/mvp")
    assert created.status_code == 201
    assert created.json()["version"] == 1

    latest = await client.get(f"/api/v1/projects/{project_id}/mvp")
    assert latest.status_code == 200
    assert latest.json()["spec"]["objective"]


async def test_mvp_without_intelligence_conflicts(client):
    project_id = (await client.post("/api/v1/projects", json={"name": "Empty"})).json()["id"]
    resp = await client.post(f"/api/v1/projects/{project_id}/mvp")
    assert resp.status_code == 409
