from fastapi.testclient import TestClient
from app.main import app


def test_root_should_return_message():
    client = TestClient(app)
    response = client.get("/")
    assert response.json() == {"message": "Hello World"}
    assert response.status_code == 200