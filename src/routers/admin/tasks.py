from fastapi import APIRouter, UploadFile, File, Form
from src.services.tasks_service import TasksService
from src.schemas.tasks import TaskCreateUpdateSchema
from src.routers.dependencies import DBDep, AuthUserDep, QueryParamsDep

router = APIRouter(prefix="/tasks")


@router.post("/")
async def post_task(
        db: DBDep,
        user: AuthUserDep,
        title: str = Form(...),
        description: str | None = Form(None),
        department_id: int | None = Form(None),
        executor_ids: list[int] = Form([]),
        attachments: list[UploadFile] = Form([])
    ):
    return await TasksService(db).create_task(
        user_id=user.user_id,
        title=title,
        description=description,
        department_id=department_id,
        attachments=attachments,
        executor_ids=executor_ids
    )


@router.get("/")
async def get_tasks(db: DBDep, query_params: QueryParamsDep):
    res = await TasksService(db).get_tasks(query_params)
    return res


@router.put("/{id}")
async def put_task(
        id: int,
        db: DBDep,
        user: AuthUserDep,
        title: str = Form(...),
        description: str | None = Form(None),
        department_id: int | None = Form(None),
        executor_ids: list[int] = Form([]),
        attachments: list[UploadFile] = Form([])
):
    task = await TasksService(db).update_task(
        author_id=user.id,
        task_id=id,
        title=title,
        description=description,
        department_id=department_id,
        attachments=attachments,
        executor_ids=executor_ids
    )
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