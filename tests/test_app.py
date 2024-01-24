from app.schemas import UserSchemaRes


def test_root_should_return_message(client):
    response = client.get("/")
    assert response.json() == {"message": "Hello World"}
    assert response.status_code == 200


def test_create_user(client):
    user_data = {"username": "Jeh", "email": "jeh@email.com", "password": "secret"}

    response = client.post("/users", json=user_data)

    assert response.status_code == 201
    assert response.json() == {"id": 1, "username": "Jeh", "email": "jeh@email.com"}


def test_create_user_already_exists(client, user):
    user_data = {"username": "Jeh", "email": "jeh@email.com", "password": "secret"}

    response = client.post("/users", json=user_data)

    assert response.status_code == 400


def test_get_list_users_empty(client):
    response = client.get("/users")

    assert response.status_code == 200
    assert response.json() == {"users": []}


def test_get_list_users(client, user):
    user_schema = UserSchemaRes.model_validate(user).model_dump()
    response = client.get("/users")

    assert response.json() == {"users": [user_schema]}


def test_update_user(client, user):
    response = client.patch(
        "/users/1",
        json={"username": "Raffa", "email": "raffa@email.com", "password": "secret"},
    )

    assert response.status_code == 200
    assert response.json() == {"id": 1, "username": "Raffa", "email": "raffa@email.com"}


def test_update_user_not_found(client, user):
    response = client.patch(
        "/users/2",
        json={"username": "Raffa", "email": "raffa@email.com", "password": "secret"},
    )

    assert response.status_code == 404


def test_delete_user(client, user):
    response = client.delete("/users/1")

    assert response.status_code == 200
    assert response.json() == {"detail": "User deleted"}


def test_delete_user_not_found(client, user):
    response = client.delete("/users/2")

    assert response.status_code == 404


def test_generate_access_token(client, user):
    response = client.post(
        "/token", data={"username": user.email, "password": user.clean_password}
    )

    token = response.json()

    assert response.status_code == 200
    assert "access_token" in token
    assert "token_type" in token
