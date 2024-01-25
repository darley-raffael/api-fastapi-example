from app.security import create_access_token
from jose import jwt
from app.settings import Settings

settings = Settings()


def test_create_access_token():
    data = {"username": "Jeh", "email": "jeh@email.com"}
    access_token = create_access_token(data)
    decode = jwt.decode(
        access_token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
    )

    assert decode["email"] == data["email"]
    assert decode["exp"]
