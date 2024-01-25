from typing import Annotated
from sqlalchemy import select
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from app.database import get_session
from app.models import User
from app.schemas import Token
from app.security import create_access_token, password_verify

OAuth2Form = Annotated[OAuth2PasswordRequestForm, Depends()]
Session = Annotated[Session, Depends(get_session)]


router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/token", response_model=Token)
async def login_for_access_token(
    form_data: OAuth2Form,
    session: Session,
):
    user = session.scalar(select(User).where(User.email == form_data.username))

    if not user:
        raise HTTPException(status_code=400, detail="Incorrect email or password")

    if not password_verify(form_data.password, user.password):
        raise HTTPException(status_code=400, detail="Incorrect email or password")

    access_token = create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}
