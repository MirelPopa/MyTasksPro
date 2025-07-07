# tests/test_auth.py

import pytest

@pytest.mark.asyncio
async def test_signup_and_login(client):
    # Signup
    res = await client.post("/signup", json={
        "email": "test@example.com",
        "password": "secret"
    })
    assert res.status_code == 200
    assert "access_token" in res.json()

    # Login
    res = await client.post("/login", json={
        "email": "test@example.com",
        "password": "secret"
    })
    assert res.status_code == 200
    data = res.json()
    assert "access_token" in data
