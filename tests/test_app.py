def test_root_should_return_message(client):
    response = client.get("/")
    assert response.json() == {"message": "Hello World"}
    assert response.status_code == 200


def test_create_user(client):
    user_data = {"username": "Jeh", "email": "jeh@email.com", "password": "secret"}

    response = client.post("/users", json=user_data)

    assert response.status_code == 201
    assert response.json() == {"id": 1, "username": "Jeh", "email": "jeh@email.com"}


def test_get_list_users(client):
    response = client.get("/users")

    assert response.status_code == 200
    assert response.json() == {
        "users": [{"id": 1, "username": "Jeh", "email": "jeh@email.com"}]
    }


def test_update_user(client):
    response = client.patch(
        "/users/1",
        json={"username": "Raffa", "email": "raffa@email.com", "password": "secret"},
    )

    assert response.status_code == 200
    assert response.json() == {"id": 1, "username": "Raffa", "email": "raffa@email.com"}


def test_update_user_not_found(client):
    response = client.patch(
        "/users/2",
        json={"username": "Raffa", "email": "raffa@email.com", "password": "secret"},
    )

    assert response.status_code == 404


def test_delete_user(client):
    response = client.delete("/users/1")

    assert response.status_code == 200
    assert response.json() == {"detail": "User deleted"}


def test_delete_user_not_found(client):
    response = client.delete("/users/2")

    assert response.status_code == 404
