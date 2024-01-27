from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session as Se
from sqlalchemy import select
from app.database import get_session
from app.models import User

from app.schemas import Message, UserList, UserSchemaReq, UserSchemaRes
from app.security import get_current_user, password_hash

router = APIRouter(prefix="/users", tags=["users"])

Session = Annotated[Se, Depends(get_session)]
CurrentUser = Annotated[User, Depends(get_current_user)]


@router.post("/", status_code=201, response_model=UserSchemaRes)
async def create_user(user: UserSchemaReq, session: Session):  # type: ignore
    db_user = session.scalar(select(User).where(User.username == user.username))

    if db_user:
        raise HTTPException(status_code=400, detail="User already exists")

    hashed_password = password_hash(user.password)
    db_user = User(username=user.username, email=user.email, password=hashed_password)

    session.add(db_user)
    session.commit()
    session.refresh(db_user)

    return db_user


@router.get("/", response_model=UserList)
async def get_users(session: Session, skip: int = 0, limit: int = 100):
    users = session.scalars(select(User).offset(skip).limit(limit)).all()
    return {"users": users}


@router.patch("/{user_id}", response_model=UserSchemaRes)
async def update_user(
    user_id: int,
    user: UserSchemaReq,
    session: Session,
    current_user: CurrentUser,
):
    if current_user.id != user_id:
        raise HTTPException(status_code=400, detail="Not enough permissions")

    current_user.username = user.username
    current_user.email = user.email
    current_user.password = password_hash(user.password)
    session.commit()
    session.refresh(current_user)

    return current_user


@router.delete("/{user_id}", response_model=Message)
async def delete_user(
    user_id: int,
    session: Session,
    current_user: CurrentUser,
):
    if current_user.id != user_id:
        raise HTTPException(status_code=400, detail="Not enough permissions")

    session.delete(current_user)
    session.commit()

    return {"detail": "User deleted"}
