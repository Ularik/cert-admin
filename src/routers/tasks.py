from fastapi import APIRouter
from src.routers.dependencies import AuthUserDep


router = APIRouter(prefix="/tasks", tags=["Ручки задач сортрудников"])


@router.post("/")
async def post_task_reply(
        user: AuthUserDep,

):
    # исполнить задачу (создать taskReply, taskReplyDocument) стать исполнителем задачи, дать комментарий
    pass
