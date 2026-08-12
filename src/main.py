from fastapi import FastAPI, Depends
from src.routers.admin.main import router as admin_router
from src.routers.dependencies import get_admin_user
from src.routers.users import router as user_router
from src.logging_conf.logging_conf import setup_logging
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    setup_logging()
    yield

app = FastAPI(lifespan=lifespan)

app.include_router(admin_router,
                   prefix="/admin",
                   tags=["admin"],
                   dependencies=[Depends(get_admin_user)],
                   responses={403: {"description": "Forbidden"}},
                   )

app.include_router(user_router)