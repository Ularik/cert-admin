from fastapi import APIRouter


router = APIRouter(prefix="/tasks")

@router.post("/")
async def post_task():
    # прикрепить документ
    # уведомить начальников отделов
    pass

@router.put("/{id}")
async def put_task():
    # изменить задачу только свою
    # не поручать тут
    pass

@router.patch("/{id}")
async def patch_task():
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