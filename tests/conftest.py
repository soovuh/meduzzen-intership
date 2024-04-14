import pytest
from fastapi.testclient import TestClient
from httpx import AsyncClient, ASGITransport

from app.db.database import create_sessionmaker, get_session, get_session_imp
from sqlalchemy.ext.asyncio import create_async_engine

from app.main import app


def register_test_db(app):
    test_engine = create_async_engine("sqlite+aiosqlite:///:memory:")
    test_sessionmaker = create_sessionmaker(test_engine)

    app.dependency_overrides[get_session] = get_session_imp(test_sessionmaker)


@pytest.fixture
def sync_client():
    """Create TestClient instance"""
    client = TestClient(app=app)
    return client


@pytest.fixture
async def async_client():
    """
    Create an AsyncClient instance for testing asynchronous endpoints.
    """

    register_test_db(app)

    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://testserver"
    ) as client:
        yield client
