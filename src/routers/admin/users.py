from fastapi import APIRouter

from src.routers.dependencies import DBDep

router = APIRouter(prefix="/users")


@router.post("/")
async def set_head_of_department(
        db: DBDep,
        data: DepartmentCreateSchema
):
    res = await DepartmentService(db).add_department(data)
    return res

