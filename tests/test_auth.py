# tests/test_auth.py

def test_signup_and_login(client):
    # Signup
    res = client.post("/signup", json={
        "email": "test@example.com",
        "password": "secret"
    })
    assert res.status_code == 200
    assert "access_token" in res.json()

    # Login
    res = client.post("/login", json={
        "email": "test@example.com",
        "password": "secret"
    })
    assert res.status_code == 200
    data = res.json()
    assert "access_token" in data

def test_print_db_url():
    import os
    print("DB URL:", os.getenv("DATABASE_URL"))
    assert os.getenv("DATABASE_URL") is not None
