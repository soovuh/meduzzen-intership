def test_create_user(test_client):
    user_data = {
        "name": "John Doe",
        "email": "john.doe@example.com",
        "password": "securepassword",
    }

    response = test_client.post("/users/", json=user_data)

    assert response.status_code == 200
    assert response.json()["name"] == user_data["name"]
    assert response.json()["email"] == user_data["email"]


def test_update_user(test_client):
    user_data = {"name": "Jack Doe"}

    response = test_client.put("/users/1", json=user_data)

    assert response.status_code == 200
    assert response.json()["name"] == user_data["name"]


def test_read_user(test_client):
    response = test_client.get("/users/1")
    assert response.status_code == 200
    assert response.json()["name"] == "Jack Doe"


def test_read_users(test_client):
    response = test_client.get("/users/")
    assert response.status_code == 200
    assert len(response.json()["users"]) > 0


def test_delete_user(test_client):
    response = test_client.delete("/users/1")
    assert response.status_code == 200
