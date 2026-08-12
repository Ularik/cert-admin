from fastapi import APIRouter
from src.routers.dependencies import DBDep
from src.schemas.departments import DepartmentCreateSchema

router = APIRouter(prefix="/departments", tags=["Создание и изменение Отделов"])


@router.post("/")
async def post_departments(
        db: DBDep,
        data: DepartmentCreateSchema
):
    res = await db.departments.add_obj(data)
    await db.save()
    return res