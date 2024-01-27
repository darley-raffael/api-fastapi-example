from fastapi.testclient import TestClient
import factory
from app.models import User
import pytest
from sqlalchemy import StaticPool, create_engine
from sqlalchemy.orm import sessionmaker
from app.main import app
from app.models import Base
from app.database import get_session
from app.security import password_hash


@pytest.fixture
def client(session):
    def get_session_override():
        return session

    with TestClient(app) as client:
        app.dependency_overrides[get_session] = get_session_override
        yield client

    app.dependency_overrides.clear()


@pytest.fixture
def session():
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    Session = sessionmaker(bind=engine)
    Base.metadata.create_all(engine)
    yield Session()
    Base.metadata.drop_all(engine)


class UserFactory(factory.Factory):
    class Meta:
        model = User

    id = factory.Sequence(lambda n: n)
    username = factory.LazyAttribute(lambda obj: f"user-{obj.id}")
    email = factory.LazyAttribute(lambda obj: f"{obj.username}@example.com")
    password = factory.LazyAttribute(lambda obj: f"{obj.username}@test.com")


@pytest.fixture
def user(session):
    password = "secret"
    user = UserFactory(password=password_hash(password))
    session.add(user)
    session.commit()
    session.refresh(user)

    user.clean_password = password
    return user


@pytest.fixture
def other_user(session):
    password = "secret"
    user = UserFactory(password=password_hash(password))

    session.add(user)
    session.commit()
    session.refresh(user)

    user.clean_password = "secret"

    return user


@pytest.fixture
def token(client, user):
    response = client.post(
        "auth/token", data={"username": user.email, "password": user.clean_password}
    )
    return response.json()["access_token"]
