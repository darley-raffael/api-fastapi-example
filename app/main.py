from fastapi import Depends, FastAPI, HTTPException
from app.security import get_current_user
from fastapi.security import OAuth2PasswordRequestForm
from app.models import User
from sqlalchemy import select
from app.database import get_session
from app.schemas import Message, Token, UserList, UserSchemaReq, UserSchemaRes
from sqlalchemy.orm import Session
from app.security import create_access_token, password_hash, password_verify
from app.settings import Settings


app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


database = []


@app.post("/users", status_code=201, response_model=UserSchemaRes)
async def create_user(user: UserSchemaReq, session: Session = Depends(get_session)):
    db_user = session.scalar(select(User).where(User.username == user.username))

    if db_user:
        raise HTTPException(status_code=400, detail="User already exists")

    hashed_password = password_hash(user.password)
    db_user = User(username=user.username, email=user.email, password=hashed_password)

    session.add(db_user)
    session.commit()
    session.refresh(db_user)

    return db_user


@app.get("/users", response_model=UserList)
async def get_users(
    skip: int = 0, limit: int = 100, session: Session = Depends(get_session)
):
    users = session.scalars(select(User).offset(skip).limit(limit)).all()
    return {"users": users}


@app.patch("/users/{user_id}", response_model=UserSchemaRes)
async def update_user(
    user_id: int,
    user: UserSchemaReq,
    session: Session = Depends(get_session),
    current_user=Depends(get_current_user),
):
    if current_user.id != user_id:
        raise HTTPException(status_code=400, detail="Not enough permissions")

    current_user.username = user.username
    current_user.email = user.email
    current_user.password = password_hash(user.password)
    session.commit()
    session.refresh(current_user)

    return current_user


@app.delete("/users/{user_id}", response_model=Message)
async def delete_user(
    user_id: int,
    session: Session = Depends(get_session),
    current_user=Depends(get_current_user),
):
    if current_user.id != user_id:
        raise HTTPException(status_code=400, detail="Not enough permissions")

    session.delete(current_user)
    session.commit()

    return {"detail": "User deleted"}


@app.get("/info")
async def info():
    return {"database_name": Settings().DATABASE_URL}


@app.post("/token", response_model=Token)
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    session: Session = Depends(get_session),
):
    user = session.scalar(select(User).where(User.email == form_data.username))

    if not user:
        raise HTTPException(status_code=400, detail="Incorrect email or password")

    if not password_verify(form_data.password, user.password):
        print(user.password)
        print(form_data.password)
        raise HTTPException(status_code=400, detail="Incorrect email or password")

    access_token = create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}
