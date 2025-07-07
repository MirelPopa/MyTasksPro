# tests/test_tasks.py

import pytest

@pytest.mark.asyncio
async def test_create_and_get_task(client):
    # Signup + Login
    await client.post("/signup", json={"email": "user1@example.com", "password": "pw"})
    login = await client.post("/login", json={"email": "user1@example.com", "password": "pw"})
    token = login.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # Create Task
    res = await client.post("/tasks/", headers=headers, json={
        "title": "Test Task",
        "description": "Test Desc",
        "priority": 3
    })
    assert res.status_code == 200
    task_id = res.json()["task_id"]

    # Get Task
    res = await client.get(f"/tasks/{task_id}", headers=headers)
    assert res.status_code == 200
    task = res.json()
    assert task["title"] == "Test Task"
