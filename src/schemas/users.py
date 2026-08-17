from pydantic import BaseModel, Field, ConfigDict
from typing import Literal


class UsersRequestSchema(BaseModel):
    username: str
    last_name: str
    status: Literal["ADMIN", "HEAD", "USER"] = Field(default="USER")
    password: str


class UserLoginSchema(BaseModel):
    username: str
    last_name: str
    password: str


class UserInCookiesSchema(BaseModel):
    user_id: int
    status: str


class UserAddSchema(BaseModel):
    username: str
    last_name: str
    status: str
    hashed_password: bytes


class UserOutSchema(BaseModel):
    id: int
    username: str
    last_name: str
    status: str
    department: int | None
    model_config = ConfigDict(from_attributes=True)


class UserUpdateSchema(BaseModel):
    username: str | None = None
    last_name: str | None = None
    status: str | None = None
    department: int | None = None


class UserHashedPswdSchema(UserAddSchema):
    id: int
    model_config = ConfigDict(from_attributes=True)
