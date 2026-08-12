from pydantic import BaseModel, Field, ConfigDict
from typing import Literal
from src.models.users import UserStatus


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
    model_config = ConfigDict(from_attributes=True)


class UserHashedPswdSchema(UserAddSchema):
    id: int

    model_config = ConfigDict(from_attributes=True)
