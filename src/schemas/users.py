from pydantic import BaseModel, Field, ConfigDict
from typing import Literal


class UsersAuthSchema(BaseModel):
    username: str
    last_name: str
    status: Literal["ADMIN", "HEAD", "DEPUTY", "USER"] = Field(default="USER")
    department: int | None = None
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
    department: int | None = None
    hashed_password: bytes

    model_config = ConfigDict(from_attributes=True, extra='ignore')


class UserOutSchema(BaseModel):
    id: int
    username: str
    last_name: str
    status: str
    department: int | None
    model_config = ConfigDict(from_attributes=True)


class UserWithDepartmentOut(BaseModel):
    id: int
    username: str
    last_name: str | None = None
    status: str
    department_id: int | None = None
    member_department: str | None = None     # Где работает
    head_of_department: str | None = None      # Где начальник
    deputy_head_of_department: str | None = None # Где зам

    model_config = ConfigDict(from_attributes=True, extra="ignore")


class UserUpdateSchema(BaseModel):
    username: str | None = None
    last_name: str | None = None
    status: str | None = None
    department: int | None = None


class UserHashedPswdSchema(UserAddSchema):
    id: int
    model_config = ConfigDict(from_attributes=True)
