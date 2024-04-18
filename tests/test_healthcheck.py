def test_health_check(test_client):
    """Test the health_check endpoint."""
    response = test_client.get("/healthcheck")
    assert response.status_code == 200
    assert response.json() == {"status": 200, "detail": "ok", "result": "working"}


def test_health_check_db(test_client):
    response = test_client.get("/healthcheck/db")
    assert response.status_code == 200
    assert response.json() == {
        "status": 200,
        "detail": "Database connection is working",
        "result": "working",
    }


def test_health_check_redis(test_client):
    response = test_client.get("/healthcheck/redis")
    assert response.status_code == 200
    assert response.json() == {
        "status": 200,
        "detail": "Redis connection is working",
        "result": "working",
    }
