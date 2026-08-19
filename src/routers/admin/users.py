from fastapi import APIRouter
from src.routers.dependencies import DBDep
from src.schemas.users import UserAddSchema, UsersAuthSchema
from src.services.user_service import UserService


router = APIRouter(prefix="/users")


@router.post("/")
async def add_user(
        db: DBDep,
        data: UsersAuthSchema
):
    res = await UserService(db).create_user(data)
    return res

