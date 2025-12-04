import pytest
from httpx import AsyncClient

# 1. Test Registration


@pytest.mark.asyncio
async def test_create_user(client: AsyncClient):
    response = await client.post("/auth/register", json={
        "email": "test@example.com",
        "password": "strongpassword123"
    })
    assert response.status_code == 201
    assert response.json()["email"] == "test@example.com"

# 2. Test Login & Token


@pytest.mark.asyncio
async def test_login_and_get_token(client: AsyncClient):
    # Register first (tests are isolated, so we re-register or use a fixture)
    await client.post("/auth/register", json={
        "email": "user2@example.com",
        "password": "password"
    })

    # Login (Form Data, not JSON!)
    response = await client.post("/auth/token", data={
        "username": "user2@example.com",
        "password": "password"
    })
    assert response.status_code == 200
    token = response.json()["access_token"]
    assert token is not None
    return token

# 3. Test Creating a Task (Authenticated)


@pytest.mark.asyncio
async def test_create_task(client: AsyncClient):
    # Setup: Register & Login
    await client.post("/auth/register", json={"email": "task@user.com", "password": "pw"})
    login_res = await client.post("/auth/token", data={"username": "task@user.com", "password": "pw"})
    token = login_res.json()["access_token"]

    # Act: Create Task
    headers = {"Authorization": f"Bearer {token}"}
    response = await client.post("/tasks/", json={
        "title": "Automated Test Task",
        "description": "Running via Pytest"
    }, headers=headers)

    # Assert
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Automated Test Task"
    assert data["owner_id"] is not None


@pytest.mark.asyncio
async def test_pagination(client: AsyncClient):
    # 1. Setup
    email = "pagination@example.com"
    password = "password"
    await client.post("/auth/register", json={"email": email, "password": password})
    login_res = await client.post("/auth/token", data={"username": email, "password": password})
    token = login_res.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # 2. Create 15 tasks with Assertion
    for i in range(15):
        res = await client.post("/tasks/", json={"title": f"Task {i}"}, headers=headers)
        # DEBUG: Stop immediately if creation fails
        assert res.status_code == 201, f"Failed to create Task {i}: {res.text}"

    # 3. Test Limit
    response = await client.get("/tasks/?limit=5&skip=0", headers=headers)
    data = response.json()
    assert len(data) == 5
