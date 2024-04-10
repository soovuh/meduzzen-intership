import pytest
from fastapi.testclient import TestClient
from app.main import app


@pytest.fixture
def test_app():
    """Create TestClient instance"""
    client = TestClient(app=app)
    return client
