from fastapi import FastAPI, HTTPException
from app.users.schemas import Message, UserDB, UserList, UserSchemaReq, UserSchemaRes


app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


database = []


@app.post("/users", status_code=201, response_model=UserSchemaRes)
async def create_user(user: UserSchemaReq):
    user_with_id = UserDB(**user.model_dump(), id=len(database) + 1)
    database.append(user_with_id)
    return user_with_id


@app.get("/users", response_model=UserList)
async def get_users():
    return {"users": database}


@app.patch("/users/{user_id}", response_model=UserSchemaRes)
async def update_user(user_id: int, user: UserSchemaReq):
    if user_id > len(database) or user_id < 1:
        raise HTTPException(status_code=404, detail="User not found")

    user_with_id = UserDB(**user.model_dump(), id=user_id)

    database[user_id - 1] = user_with_id

    return user_with_id


@app.delete("/users/{user_id}", response_model=Message)
async def delete_user(user_id: int):
    if user_id > len(database) or user_id < 1:
        raise HTTPException(status_code=404, detail="User not found")

    del database[user_id - 1]

    return {"detail": "User deleted"}
