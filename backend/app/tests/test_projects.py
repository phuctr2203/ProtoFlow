import uuid

from httpx import AsyncClient


async def test_create_project(client: AsyncClient) -> None:
    resp = await client.post("/api/v1/projects", json={"name": "Acme Corp"})
    assert resp.status_code == 201
    body = resp.json()
    assert body["name"] == "Acme Corp"
    assert body["status"] == "DISCOVERY"
    assert "id" in body


async def test_get_project(client: AsyncClient) -> None:
    created = (await client.post("/api/v1/projects", json={"name": "Beta"})).json()
    resp = await client.get(f"/api/v1/projects/{created['id']}")
    assert resp.status_code == 200
    assert resp.json()["id"] == created["id"]


async def test_list_projects(client: AsyncClient) -> None:
    await client.post("/api/v1/projects", json={"name": "One"})
    await client.post("/api/v1/projects", json={"name": "Two"})
    resp = await client.get("/api/v1/projects")
    assert resp.status_code == 200
    assert len(resp.json()) == 2


async def test_get_unknown_project_returns_404(client: AsyncClient) -> None:
    resp = await client.get(f"/api/v1/projects/{uuid.uuid4()}")
    assert resp.status_code == 404


async def test_create_project_rejects_empty_name(client: AsyncClient) -> None:
    resp = await client.post("/api/v1/projects", json={"name": ""})
    assert resp.status_code == 422
