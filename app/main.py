from fastapi import FastAPI
from app.routes import users, auth

app = FastAPI()

app.include_router(users.router)
app.include_router(auth.router)


@app.get("/")
async def root():
    return {"message": "Hello World"}
