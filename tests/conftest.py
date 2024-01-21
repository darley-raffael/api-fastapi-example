from fastapi.testclient import TestClient
import pytest
from app.main import app

@pytest.fixture
def client():
    client = TestClient(app)
    return client