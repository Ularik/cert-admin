from fastapi import APIRouter, HTTPException, Response
from src.schemas.users import UsersRequestSchema, UserAddSchema, UserLoginSchema, UserInCookiesSchema
from src.repositories.users_repository import UsersRepository
from src.database import AsyncSessionMaker
from src.services.auth import AuthService
from src.routers.dependencies import DBDep, AuthUserDep
from src.exceptions.exceptions import UniqueObjIsExistException


router = APIRouter(prefix="/users", tags=["Пользователи"])


@router.post("/login")
async def login_user(db: DBDep, data: UserLoginSchema, response: Response):
    user = await db.users.get_user_with_hashed_pswd(username=data.username, last_name=data.last_name)
    if not user:
        raise HTTPException(status_code=401, detail="Пользователь не найден")
    if not await AuthService().verify_password(data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Неверный пароль!")

    payload = UserInCookiesSchema(**{"user_id": user.id, "status": user.status})
    access_token = await AuthService().create_access_token(payload)
    response.set_cookie("access_token", access_token, secure=False)
    return {"access_token": access_token}


@router.post("/", summary="Добавление нового пользователя")
async def add_user(db: DBDep, data: UsersRequestSchema):
    hashed_password = await AuthService().hash_pswd(data.password)
    new_data = UserAddSchema(
        username=data.username, last_name=data.last_name,
        status=data.status, hashed_password=hashed_password
    )
    try:
        new_user = await db.users.add_obj(new_data)
        await db.save()
    except UniqueObjIsExistException as err:
        raise HTTPException(status_code=409, detail=err.detail)
    return new_user


@router.get("/")
async def get_users():
    async with AsyncSessionMaker() as session:
        users = await UsersRepository(session).get_objects()
    return users


@router.get("/me")
async def get_me(user_id: AuthUserDep):
    return {"user_id": user_id}


@router.post("/logout")
async def logout(response: Response):
    response.delete_cookie("access_token")
    return {"success": "Вы вышли из аккаунта"}
