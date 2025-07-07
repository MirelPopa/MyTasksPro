import pytest
from fastapi.testclient import TestClient
from api.main import fast_api_app
from db.main import get_db

@pytest.fixture
def client(db_session):
    def override_get_db():
        yield db_session

    fast_api_app.dependency_overrides[get_db] = override_get_db

    with TestClient(fast_api_app) as c:
        yield c
