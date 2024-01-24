from app.security import ALGORITHM, SECRET_KEY, create_access_token
from jose import jwt


def test_create_access_token():
    data = {"username": "Jeh", "email": "jeh@email.com"}
    access_token = create_access_token(data)
    decode = jwt.decode(access_token, SECRET_KEY, algorithms=[ALGORITHM])

    assert decode["email"] == data["email"]
    assert decode["exp"]
