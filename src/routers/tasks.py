import urllib

from fastapi import APIRouter, HTTPException, Response, Form, UploadFile

from src.routers.dependencies import AuthUserDep, DBDep, QueryParamsDep
from src.services.reply_service import ReplyService
from src.services.tasks_service import TasksService
from src.services.documents_service import DocumentService

router = APIRouter(prefix="/tasks", tags=["Ручки задач сортрудников"])


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

@router.get("/task-documents/{doc_id}/download")
async def download_task_document(doc_id: int, db: DBDep):
    doc = await DocumentService(db).download_task_document(document_id=doc_id)
    if not doc:
        raise HTTPException(status_code=404, detail="Документ не найден")

    encoded_filename = urllib.parse.quote(doc.filename)

    return Response(
        content=doc.file_data,
        media_type=doc.mime_type,
        headers={
            "Content-Disposition": f"attachment; filename*=UTF-8''{encoded_filename}"
        }
    )

@router.get("/reply-documents/{doc_id}/download")
async def download_reply_document(doc_id: int, db: DBDep):
    doc = await DocumentService(db).download_reply_document(document_id=doc_id)
    if not doc:
        raise HTTPException(status_code=404, detail="Документ не найден")

    encoded_filename = urllib.parse.quote(doc.filename)

    return Response(
        content=doc.file_data,
        media_type=doc.mime_type,
        headers={
            "Content-Disposition": f"attachment; filename*=UTF-8''{encoded_filename}"
        }
    )


@router.get("/")
async def get_tasks(db: DBDep, query_params: QueryParamsDep):
    res = await TasksService(db).get_tasks(query_params)
    return res


@router.get("/{id}")
async def get_task_detail(db: DBDep, id: int):
    res = await TasksService(db).get_one(task_id=id)
    return res


@router.delete("/{id}")
async def delete_own_task(
        db: DBDep,
        id: int,
        user: AuthUserDep,
):
    # удалить только свою задач
    await TasksService(db).delete_task(task_id=id, user_id=user.user_id)
    return 200, {'status': 'delete success'}