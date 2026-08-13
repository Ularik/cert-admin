from typing import Annotated
from src.database import AsyncSessionMaker
from src.schemas.users import UserInCookiesSchema
from src.db_manager.db_manager import DbManager
from fastapi import Depends, Request, HTTPException, status
from src.services.auth import AuthService

async def get_db():
    async with DbManager(session_factory=AsyncSessionMaker) as db:
        yield db


DBDep = Annotated[DbManager, Depends(get_db)]


def get_token(request: Request) -> str:
    token = request.cookies.get("access_token", None)
    if not token:
        raise HTTPException(status_code=401, detail="Вы не передали токен аутентификации")
    return token


async def get_current_user(token: str = Depends(get_token)) -> UserInCookiesSchema:
    user_data = await AuthService.decode_token(token)
    return user_data


AuthUserDep = Annotated[UserInCookiesSchema, Depends(get_current_user)]


async def get_admin_user(user_data: UserInCookiesSchema = Depends(get_current_user)) -> UserInCookiesSchema:
    if user_data.status != "ADMIN":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Недостаточно прав для выполнения операции"
        )
    return user_data

async def get_head_user(user_data: UserInCookiesSchema = Depends(get_current_user)) -> UserInCookiesSchema:
    if user_data.status != "HEAD":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Недостаточно прав для выполнения операции"
        )
    return user_data

