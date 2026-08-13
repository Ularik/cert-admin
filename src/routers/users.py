from fastapi import APIRouter, Response
from src.schemas.users import UsersRequestSchema, UserLoginSchema
from src.services.user_service import UserService
from src.routers.dependencies import DBDep, AuthUserDep


router = APIRouter(prefix="/users", tags=["Пользователи"])


@router.post("/login")
async def login_user(db: DBDep, data: UserLoginSchema, response: Response):
    access_token = await UserService(db).login_user(data)
    response.set_cookie("access_token", access_token, secure=False)
    return {"access_token": access_token}


@router.post("/", summary="Добавление нового пользователя")
async def add_user(db: DBDep, data: UsersRequestSchema):
    return await UserService(db).create_user(data)


@router.get("/")
async def get_users(db: DBDep):
    return await UserService(db).get_users()


@router.get("/me")
async def get_me(user: AuthUserDep):
    return user


@router.post("/logout")
async def logout(response: Response):
    response.delete_cookie("access_token")
    return {"success": "Вы вышли из аккаунта"}
