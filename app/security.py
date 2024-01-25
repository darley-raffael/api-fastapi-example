from datetime import datetime, timedelta, timezone
from sqlalchemy import select
from app.models import User
from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordBearer
from jose import JWSError, jwt
from passlib.context import CryptContext

from app.database import get_session
from app.schemas import TokenData
from app.settings import Settings

settings = Settings()


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")


def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(
        minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
    )
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM
    )
    return encoded_jwt


def password_hash(password: str):
    return pwd_context.hash(password)


def password_verify(password: str, hashed_password: str):
    return pwd_context.verify(password, hashed_password)


async def get_current_user(
    session: Session = Depends(get_session), token: str = Depends(oauth2_scheme)
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        username: str = payload.get("sub")

        if not username:
            raise credentials_exception

        token_data = TokenData(username=username)
    except JWSError:
        raise credentials_exception

    user = session.scalar(select(User).where(User.email == token_data.username))

    if not user:
        raise credentials_exception

    return user
