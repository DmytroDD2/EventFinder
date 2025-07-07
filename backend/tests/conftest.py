import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy_utils import database_exists, drop_database, create_database

from app.db import Base
from app.db.session import get_db
from app.main import app
from fastapi.testclient import TestClient

from app.users.models import User
from app.users.schemas import UserToken, Role
from app.users.security import get_current_user_token

TEST_DATABASE_URL = "postgresql://test_user:test_password@test_db:5432/test_db"


engine = create_engine(TEST_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(scope="session")  # Одна база на сесію
def test_db():
    if database_exists(TEST_DATABASE_URL):
        drop_database(TEST_DATABASE_URL)
    create_database(TEST_DATABASE_URL)

    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()

    yield db

    db.close()
    drop_database(TEST_DATABASE_URL)


def mock_get_current_user_token_user():
    return UserToken(id=1, role=Role.user)

def mock_get_current_admin_token_user():
    return UserToken(id=2, role=Role.admin)

@pytest.fixture(scope="function")
def client(test_db):

    def override_get_db():
        yield test_db
    app.dependency_overrides[get_current_user_token] = mock_get_current_user_token_user
    app.dependency_overrides[get_db] = override_get_db
    return TestClient(app)


@pytest.fixture(scope="function")
def admin(client):

    app.dependency_overrides[get_current_user_token] = mock_get_current_admin_token_user

    yield client
    app.dependency_overrides.clear()  # Очистка після тесту












