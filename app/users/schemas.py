from pydantic import BaseModel, EmailStr


class UserSchemaReq(BaseModel):
    username: str
    email: EmailStr
    password: str


class UserSchemaRes(BaseModel):
    id: int
    username: str
    email: EmailStr


class UserDB(UserSchemaReq):
    id: int


class UserList(BaseModel):
    users: list[UserSchemaRes]


class Message(BaseModel):
    detail: str
