def test_health_check(test_app):
    """Test the health_check endpoint."""
    response = test_app.get("/")
    assert response.status_code == 200
    assert response.json() == {"status": 200, "detail": "ok", "result": "working"}
