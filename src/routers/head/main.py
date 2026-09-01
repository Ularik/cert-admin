from fastapi import APIRouter
from src.routers.head.tasks import router as tasks_router
from src.routers.head.users import router as users_router

router = APIRouter()

router.include_router(tasks_router)
router.include_router(users_router)