import pytest
from main import app
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from unittest.mock import AsyncMock, patch
from core.database import (
    get_async_db,
)


@pytest.fixture
def client():
    return TestClient(app)


@pytest.fixture
def mock_db_session():
    """Fixture to mock database session"""
    session = AsyncMock()
    yield session


@pytest.fixture
def override_get_async_db(mock_db_session):
    async def _override():
        yield mock_db_session

    app.dependency_overrides[get_async_db] = _override
    yield
    app.dependency_overrides.clear()
