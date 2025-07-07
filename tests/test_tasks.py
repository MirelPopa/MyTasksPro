def test_create_and_get_task(client):
    # Signup + Login
    client.post("/signup", json={"email": "user1@example.com", "password": "pw"})
    login = client.post("/login", json={"email": "user1@example.com", "password": "pw"})
    token = login.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # Create Task
    res = client.post("/tasks/", headers=headers, json={
        "title": "Test Task",
        "description": "Test Desc",
        "priority": 3
    })
    assert res.status_code == 200
    task_id = res.json()["task_id"]

    # Get Task
    res = client.get(f"/tasks/{task_id}", headers=headers)
    assert res.status_code == 200
    task = res.json()
    assert task["title"] == "Test Task"
