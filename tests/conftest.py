import os
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from db.main import Base
from api.main import fast_api_app

db_url = os.getenv("DATABASE_URL", "postgresql://admin_user:admin_pass@localhost:5432/mytasksproapp")
engine = create_engine(db_url)
TestingSessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)

@pytest.fixture(scope="session", autouse=True)
def setup_database():
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
def client(db_session):
    def override_get_db():
        yield db_session

    fast_api_app.dependency_overrides = {}  # Clear existing overrides
    fast_api_app.dependency_overrides[getattr(__import__("db.main"), "get_db")] = override_get_db

    with TestClient(fast_api_app) as c:
        yield c
