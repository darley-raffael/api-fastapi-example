from fastapi.testclient import TestClient
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import app
from app.models import Base


@pytest.fixture
def client():
    client = TestClient(app)
    return client


@pytest.fixture
def session():
    engine = create_engine("sqlite:///:memory:", echo=True)
    Session = sessionmaker(bind=engine)
    Base.metadata.create_all(engine)
    yield Session()
    Base.metadata.drop_all(engine)
