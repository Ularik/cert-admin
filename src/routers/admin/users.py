from fastapi import APIRouter, Body
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

@router.patch("/{id}")
async def set_department_user(
        db: DBDep,
        id: int,
        department_id: int = Body(..., embed=True)
):
    res = await UserService(db).set_department(id, department_id=department_id)
    return res

