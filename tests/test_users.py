from app.schemas import UserSchemaRes


def test_create_user(client):
    user_data = {"username": "Jeh", "email": "jeh@email.com", "password": "secret"}

    response = client.post("/users", json=user_data)

    assert response.status_code == 201
    assert response.json() == {"id": 1, "username": "Jeh", "email": "jeh@email.com"}


def test_create_user_already_exists(client, user):
    user_data = {
        "username": user.username,
        "email": user.email,
        "password": user.password,
    }

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


def test_update_user(client, user, token):
    response = client.patch(
        f"/users/{user.id}",
        headers={"Authorization": f"Bearer {token}"},
        json={"username": "Raffa", "email": "raffa@email.com", "password": "secret"},
    )

    assert response.status_code == 200
    assert response.json() == {
        "id": user.id,
        "username": "Raffa",
        "email": "raffa@email.com",
    }


def test_update_user_not_found(client, user, token):
    response = client.patch(
        "/users/2",
        headers={"Authorization": f"Bearer {token}"},
        json={"username": "Raffa", "email": "raffa@email.com", "password": "secret"},
    )

    assert response.status_code == 400


def test_delete_user(client, user, token):
    response = client.delete(
        f"/users/{user.id}", headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 200
    assert response.json() == {"detail": "User deleted"}


def test_delete_user_not_found(client, user, token):
    response = client.delete("/users/2", headers={"Authorization": f"Bearer {token}"})

    assert response.status_code == 400


def test_update_user_with_wrong_user(client, other_user, token):
    response = client.patch(
        f"/users/{other_user.id}",
        headers={"Authorization": f"Bearer {token}"},
        json={"username": "Raffa", "email": "raffa@email.com", "password": "secret"},
    )

    assert response.status_code == 400
    assert response.json() == {"detail": "Not enough permissions"}


def test_delete_user_with_wrong_user(client, other_user, token):
    response = client.delete(
        f"/users/{other_user.id}", headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 400
    assert response.json() == {"detail": "Not enough permissions"}
