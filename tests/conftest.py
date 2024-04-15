import pytest
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import create_async_engine
from fastapi.testclient import TestClient
from fakeredis.aioredis import FakeRedis

from app.db.database import create_sessionmaker, get_session, get_session_imp
from app.db.redis import get_redis_imp, get_redis
from app.main import app


def register_test_db(app):
    test_engine = create_async_engine("sqlite+aiosqlite:///:memory:")
    test_sessionmaker = create_sessionmaker(test_engine)

    app.dependency_overrides[get_session] = get_session_imp(test_sessionmaker)


async def get_test_redis():
    redis = await FakeRedis.from_url('redis://mock_redis')
    return redis
    

def register_test_redis(app):
    redis_fn = get_test_redis
    app.dependency_overrides[get_redis] = get_redis_imp(redis_fn)


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
    register_test_redis(app)

    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://testserver"
    ) as client:
        yield client
