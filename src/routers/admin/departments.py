from fastapi import APIRouter
from src.routers.dependencies import DBDep
from src.schemas.departments import DepartmentCreateUpdateSchema
from src.services.department_service import DepartmentService


router = APIRouter(prefix="/departments")


@router.post("/")
async def post_departments(
        db: DBDep,
        data: DepartmentCreateUpdateSchema
):
    res = await DepartmentService(db).add_department(data)
    return res


@router.put("/{id}")
async def put_department(
        db: DBDep,
        id: int,
        data: DepartmentCreateUpdateSchema
):
    res = await DepartmentService(db).update_department(dep_id=id, data=data)
    return res