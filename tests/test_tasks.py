import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_create_task_without_token_returns_401(client: AsyncClient):
    response = await client.post("/api/v1/tasks", json={"title": "Ship release"})
    assert response.status_code == 401


@pytest.mark.asyncio
async def test_create_task_with_token_returns_201(client: AsyncClient, auth_headers):
    headers = await auth_headers(client)
    response = await client.post(
        "/api/v1/tasks",
        json={"title": "Ship release", "description": "Cut v0.1"},
        headers=headers,
    )
    assert response.status_code == 201
    body = response.json()
    assert body["title"] == "Ship release"
    assert body["status"] == "pending"


@pytest.mark.asyncio
async def test_list_tasks_pagination(client: AsyncClient, auth_headers):
    headers = await auth_headers(client, email="pager@example.com")

    for i in range(5):
        await client.post("/api/v1/tasks", json={"title": f"Task {i}"}, headers=headers)

    page1 = await client.get("/api/v1/tasks?page=1&page_size=2", headers=headers)
    assert page1.status_code == 200
    data = page1.json()
    assert data["total"] == 5
    assert data["page"] == 1
    assert data["page_size"] == 2
    assert len(data["items"]) == 2

    page3 = await client.get("/api/v1/tasks?page=3&page_size=2", headers=headers)
    assert len(page3.json()["items"]) == 1


@pytest.mark.asyncio
async def test_list_tasks_status_filter(client: AsyncClient, auth_headers):
    headers = await auth_headers(client, email="filter@example.com")

    await client.post("/api/v1/tasks", json={"title": "Open"}, headers=headers)
    done = await client.post(
        "/api/v1/tasks",
        json={"title": "Closed", "status": "done"},
        headers=headers,
    )
    task_id = done.json()["id"]

    filtered = await client.get("/api/v1/tasks?status=done", headers=headers)
    items = filtered.json()["items"]
    assert len(items) == 1
    assert items[0]["id"] == task_id


@pytest.mark.asyncio
async def test_health_check(client: AsyncClient):
    response = await client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}
