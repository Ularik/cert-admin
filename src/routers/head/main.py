from fastapi import APIRouter
from src.routers.head.tasks import router as tasks_router

router = APIRouter()

router.include_router(tasks_router)