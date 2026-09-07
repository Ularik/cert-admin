from fastapi import Depends, APIRouter
from src.routers.dependencies import get_admin_user, get_head_user
from src.routers.admin.main import router as admin_router
from src.routers.head.main import router as head_router
from src.routers.users import router as user_router
from src.routers.tasks import router as router_tasks
from src.routers.reply import router as reply_router
from src.routers.departments import router as departments_router



router = APIRouter(prefix="/api")

router.include_router(admin_router,
                   prefix="/admin",
                   tags=["Ручки Главного начальника"],
                   dependencies=[Depends(get_admin_user)],
                   responses={403: {"description": "Forbidden"}},
                   )

router.include_router(head_router,
                   prefix="/head",
                   tags=["Ручки начальников"],
                   dependencies=[Depends(get_head_user)],
                   responses={403: {"description": "Forbidden"}},
                   )

router.include_router(user_router)
router.include_router(departments_router)
router.include_router(router_tasks)
router.include_router(reply_router)
