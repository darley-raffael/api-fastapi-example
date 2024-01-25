def test_root_should_return_message(client):
    response = client.get("/")
    assert response.json() == {"message": "Hello World"}
    assert response.status_code == 200
