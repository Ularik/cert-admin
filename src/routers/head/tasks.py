from fastapi import APIRouter, Form, UploadFile, Body

from src.services.reply_service import ReplyService
from src.services.tasks_service import TasksService
from src.routers.dependencies import DBDep, AuthUserDep, QueryParamsDep

router = APIRouter(prefix="/tasks")


@router.post("/")
async def post_task(
        db: DBDep,
        user: AuthUserDep,
        title: str = Form(...),
        description: str | None = Form(None),
        executor_ids: list[int] = Form([]),
        attachments: list[UploadFile] = Form([])
    ):
    return await TasksService(db).create_task(
        user_id=user.user_id,
        title=title,
        description=description,
        attachments=attachments,
        executor_ids=executor_ids
    )


@router.put("/{id}")
async def put_task(
        id: int,
        db: DBDep,
        user: AuthUserDep,
        title: str = Form(...),
        description: str | None = Form(None),
        executor_ids: list[int] = Form([]),
        attachments: list[UploadFile] = Form([]),
        old_attachments_datas: list[int] = Form([])
):
    task = await TasksService(db).update_task(
        user_id=user.user_id,
        task_id=id,
        title=title,
        description=description,
        attachments=attachments,
        old_attachments_id_from_front=old_attachments_datas,
        executor_ids=executor_ids
    )
    return task

@router.patch("/{id}")
async def patch_task(
        db: DBDep,
        id: int,
        executor_ids: list[int] = Body(..., embed=True),
):
    await TasksService(db).update_executors_task(executor_ids, task_id=id)
    # уведомить исполнителей


@router.post("/{id}/tasks_reply")
async def response_on_task(
        db: DBDep,
        user: AuthUserDep,
        id: int,
        content: str = Form(...),
        attachments: list[UploadFile] = Form([]),
):
    # исполнить задачу (создать taskReply, taskReplyDocument) стать исполнителем задачи, дать комментарий
    return await ReplyService(db).create_reply(
        executor=user,
        task_id=id,
        content=content,
        attachments=attachments
    )

@router.delete("/{id}")
async def delete_own_task(
        db: DBDep,
        id: int,
        user: AuthUserDep,
):
    # удалить только свою задач
    await TasksService(db).delete_task(task_id=id, user_id=user.user_id)
    return 200, {'status': 'delete success'}