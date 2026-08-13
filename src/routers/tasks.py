from fastapi import APIRouter
from src.routers.dependencies import AuthUserDep, DBDep


router = APIRouter(prefix="/tasks", tags=["Ручки задач сортрудников"])


@router.post("/")
async def post_task_reply(
        user: AuthUserDep,
        db: DBDep,
):
    # исполнить задачу (создать taskReply, taskReplyDocument) стать исполнителем задачи, дать комментарий
    pass

@router.get("/documents/{doc_id}/download")
async def download_document(doc_id: int, db: DBDep):
    doc = await db.task_documents.get_by_id(doc_id)
    if not doc:
        raise HTTPException(status_code=404, detail="Документ не найден")

    # Кодируем имя файла для безопасной передачи кириллицы в заголовке
    encoded_filename = urllib.parse.quote(doc.filename)

    return Response(
        content=doc.file_data,
        media_type=doc.mime_type,
        headers={
            "Content-Disposition": f"attachment; filename*=UTF-8''{encoded_filename}"
        }
    )