from fastapi import APIRouter
from src.routers.dependencies import DBDep
from src.schemas.departments import DepartmentCreateSchema
from src.services.department_service import DepartmentService

router = APIRouter(prefix="/departments")


@router.post("/")
async def post_departments(
        db: DBDep,
        data: DepartmentCreateSchema
):
    res = await DepartmentService(db).add_department(data)
    return res