import pytest


def test_health_check(sync_client):
    """Test the health_check endpoint."""
    response = sync_client.get("/healthcheck")
    assert response.status_code == 200
    assert response.json() == {"status": 200, "detail": "ok", "result": "working"}


@pytest.mark.asyncio
async def test_health_check_db(async_client):
    async for client in async_client:
        response = await client.get("/healthcheck/db")
        assert response.status_code == 200
        assert response.json() == {
            "status": 200,
            "detail": "Database connection is working",
            "result": "working",
        }


@pytest.mark.asyncio
async def test_health_check_redis(async_client):
    async for client in async_client:
        response = await client.get("/healthcheck/redis")
        assert response.status_code == 200
        assert response.json() == {
            "status": 200,
            "detail": "Redis connection is working",
            "result": "working",
        }
