from pydantic import BaseModel, ConfigDict, EmailStr


class UserSchemaReq(BaseModel):
    username: str
    email: EmailStr
    password: str


class UserSchemaRes(BaseModel):
    id: int
    username: str
    email: EmailStr

    model_config = ConfigDict(from_attributes=True)


class UserList(BaseModel):
    users: list[UserSchemaRes]


class Message(BaseModel):
    detail: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None
