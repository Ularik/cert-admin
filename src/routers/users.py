from fastapi import APIRouter, Response, Body
from src.schemas.users import UsersRequestSchema, UserLoginSchema
from src.services.user_service import UserService
from src.routers.dependencies import DBDep, AuthUserDep
from src.models.users import UserStatus


router = APIRouter(prefix="/users", tags=["Пользователи"])


@router.post("/login")
async def login_user(db: DBDep, data: UserLoginSchema, response: Response):
    access_token = await UserService(db).login_user(data)
    response.set_cookie("access_token", access_token, secure=False)
    return {"access_token": access_token}


@router.post("/", summary="Добавление нового пользователя")
async def add_user(db: DBDep, data: UsersRequestSchema):
    res = await UserService(db).create_user(data)
    return res

@router.get("/")
async def get_users(db: DBDep, department_id: int | None = None):
    return await UserService(db).get_users(department=department_id)


@router.get("/roles")
async def get_users_statuses_list():
    return [status.value for status in UserStatus]

@router.get("/me")
async def get_me(db: DBDep, user: AuthUserDep):
    user = await UserService(db).get_me(id=user.user_id)
    return user


@router.patch("/")
async def set_department_user(
        db: DBDep,
        user: AuthUserDep,
        department_id: int = Body(..., embed=True)
):
    res = await UserService(db).set_department(user.user_id, department_id=department_id)
    return res

@router.post("/logout")
async def logout(response: Response):
    response.delete_cookie("access_token")
    return {"success": "Вы вышли из аккаунта"}
