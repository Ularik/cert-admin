from fastapi import APIRouter, HTTPException, Response, Form, UploadFile

from src.routers.dependencies import DBDep, AuthUserDep
from src.services.reply_service import ReplyService

router = APIRouter(prefix="/tasks", tags=["Ответы на задачи"])


@router.get("/{id}/tasks_reply")
async def get_tasks_reply(
        db: DBDep,
        user: AuthUserDep,
        id: int,
):
    return await ReplyService(db).get_replies(task_id=id)


@router.get("/tasks_reply/{id}")
async def get_tasks_reply(
        db: DBDep,
        user: AuthUserDep,
        id: int,
):
    return await ReplyService(db).get_one_reply(reply_id=id)


@router.post("/{id}/tasks_reply")
async def response_on_task(
        db: DBDep,
        user: AuthUserDep,
        id: int,
        content: str = Form(...),
        attachments: list[UploadFile] = Form([]),
):
    return await ReplyService(db).create_reply(
        executor=user,
        task_id=id,
        content=content,
        attachments=attachments
    )

@router.delete("/tasks_reply/{id}")
async def delete_reply(
        db: DBDep,
        id: int
):
    await ReplyService(db).delete_reply(reply_id=id)
    return 200, "delete success"