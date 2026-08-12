from fastapi import APIRouter
from src.routers.admin.users import router as user_router
from src.routers.admin.departments import router as department_router

router = APIRouter()

router.include_router(user_router)
router.include_router(department_router)