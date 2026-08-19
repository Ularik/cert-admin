from fastapi import APIRouter
from src.routers.dependencies import DBDep
from src.services.department_service import DepartmentService


router = APIRouter(prefix="/departments", tags=["Отделы"])


@router.get("/")
async def get_departments(db: DBDep):
    return await DepartmentService(db).get_department()


@router.get("/{id}")
async def get_departments(
        db: DBDep,
        id: int
):
    return await DepartmentService(db).get_one_department(department_id=id)

