import pytest
from fastapi.testclient import TestClient
from fakeredis.aioredis import FakeRedis

from app.main import app, register_db, register_redis


@pytest.fixture
def test_client():
    """Create TestClient instance"""

    register_db(app)
    register_redis(app)

    client = TestClient(app=app)
    return client
