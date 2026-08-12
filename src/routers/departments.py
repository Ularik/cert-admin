from fastapi import APIRouter
from src.routers.dependencies import DBDep


router = APIRouter(prefix="/departments", tags=["Отделы"])


@router.get("/")
async def get_departments(db: DBDep):
    return await db.departments.get_objects()

