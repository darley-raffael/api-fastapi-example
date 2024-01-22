from fastapi import Depends, FastAPI, HTTPException
from app.models import User
from sqlalchemy import select
from app.database import get_session
from app.schemas import Message, UserList, UserSchemaReq, UserSchemaRes
from sqlalchemy.orm import Session
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

    db_user = User(username=user.username, email=user.email, password=user.password)

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
    user_id: int, user: UserSchemaReq, session: Session = Depends(get_session)
):
    db_user = session.scalar(select(User).where(User.id == user_id))

    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")

    db_user.username = user.username
    db_user.email = user.email
    db_user.password = user.password
    session.commit()
    session.refresh(db_user)

    return db_user


@app.delete("/users/{user_id}", response_model=Message)
async def delete_user(user_id: int, session: Session = Depends(get_session)):
    db_user = session.scalar(select(User).where(User.id == user_id))

    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")

    session.delete(db_user)
    session.commit()

    return {"detail": "User deleted"}


@app.get("/info")
async def info():
    return {"database_name": Settings().DATABASE_URL}
