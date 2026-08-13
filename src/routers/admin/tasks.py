from fastapi import APIRouter, UploadFile, File, Form
from src.services.tasks_service import TasksService
from src.schemas.tasks import TaskCreateUpdateSchema
from src.routers.dependencies import DBDep


router = APIRouter(prefix="/tasks")


@router.post("/")
async def post_task(
    db: DBDep,
    title: str = Form(...),
    description: str | None = Form(None),
    department_id: int | None = Form(None),
    attachments: list[UploadFile] = File([]),
):
    # прикрепить документ
    # уведомить начальников отделов
    return await TasksService(db).create_task(
        title=title,
        description=description,
        department_id=department_id,
        attachments=attachments,
    )

@router.put("/{id}")
async def put_task(
        id: int,
        db: DBDep,
        data: TaskCreateUpdateSchema,
        attachments: list[UploadFile] = File([]),
):
    task = await TasksService(db).update_task(task_id=id, data=data, attachments=attachments)
    return task

@router.patch("/{id}")
async def patch_task(db: DBDep):
    # поручить исполнителей
    # уведомить исполнителей
    pass

@router.post("/{id}/tasks_reply")
async def response_on_task():
    # исполнить задачу (создать taskReply, taskReplyDocument) стать исполнителем задачи, дать комментарий
    pass

@router.delete("/{id}")
async def delete_own_task():
    # удалить только свою задачу
    pass