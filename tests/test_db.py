from sqlalchemy import select
from app.models import User


def test_create_user(session):
    new_user = User(username="Jeh", email="jeh@email.com", password="secret")
    session.add(new_user)
    session.commit()

    user = session.scalar(select(User).where(User.username == "Jeh"))

    assert user.username == "Jeh"
