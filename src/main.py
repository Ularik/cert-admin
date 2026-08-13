from fastapi import FastAPI, Depends
from src.routers.dependencies import get_admin_user, get_head_user
from src.routers.admin.main import router as admin_router
from src.routers.head.main import router as head_router
from src.routers.users import router as user_router
from src.routers.departments import router as departments_router
from src.logging_conf.logging_conf import setup_logging
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    setup_logging()
    yield

app = FastAPI(lifespan=lifespan)

app.include_router(admin_router,
                   prefix="/admin",
                   tags=["Ручки Главного начальника"],
                   dependencies=[Depends(get_admin_user)],
                   responses={403: {"description": "Forbidden"}},
                   )

app.include_router(head_router,
                   prefix="/head",
                   tags=["Ручки начальников"],
                   dependencies=[Depends(get_head_user)],
                   responses={403: {"description": "Forbidden"}},
                   )

app.include_router(user_router)
app.include_router(departments_router)