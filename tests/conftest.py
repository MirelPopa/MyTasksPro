import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

TEST_DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://admin_user:admin_pass@localhost:5432/mytasksproapp"
)

engine = create_engine(TEST_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Set up and tear down the test DB
@pytest.fixture(scope="session", autouse=True)
def setup_database():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

# Provide DB session to tests
@pytest.fixture()
def db_session():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

# Override the app’s DB dependency
@pytest.fixture()
def client(db_session):
    def override_get_db():
        yield db_session

    fast_api_app.dependency_overrides[get_db] = override_get_db

    with TestClient(fast_api_app) as c:
        yield c
