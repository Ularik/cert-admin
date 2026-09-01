from fastapi import APIRouter
from src.routers.dependencies import DBDep
from src.schemas.users import UsersAuthSchema, UserUpdateSchema
from src.services.user_service import UserService


router = APIRouter(prefix="/users")


@router.post("/")
async def add_user(
        db: DBDep,
        data: UsersAuthSchema
):
    res = await UserService(db).create_user(data)
    return res


@router.delete("/{id}")
async def delete_user(
        db: DBDep,
        id: int
):
    await UserService(db).delete_user(id)
    return 200, "deleted"


@router.patch("/{id}")
async def update_user(
        db: DBDep,
        id: int,
        data: UserUpdateSchema
):
    res = await UserService(db).update_user(data=data, user_id=id)
    return res