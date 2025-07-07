# tests/conftest.py

import pytest
from fastapi.testclient import TestClient
from httpx import AsyncClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from db.main import Base, get_db
from api.main import fast_api_app

from contextlib import asynccontextmanager
from sqlalchemy.pool import StaticPool

# SQLite in-memory test DB
TEST_DB_URL = "sqlite://"

engine = create_engine(
    TEST_DB_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool
)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Override DB dependency
@pytest.fixture(scope="session", autouse=True)
def create_test_database():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

@pytest.fixture()
def db_session():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

@pytest.fixture()
async def client(db_session):
    def override_get_db():
        yield db_session

    fast_api_app.dependency_overrides[get_db] = override_get_db

    async with AsyncClient(app=fast_api_app, base_url="http://test") as ac:
        yield ac
