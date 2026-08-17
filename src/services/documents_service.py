from src.services.base import BaseService
from src.schemas.tasks import DocumentOutSchema


class DocumentService(BaseService):

    async def download_task_document(self, document_id: int):
        res: DocumentOutSchema = await self.db.tasks_documents.download_document(id=document_id)
        return res

    async def download_reply_document(self, document_id: int):
        res: DocumentOutSchema = await self.db.reply_documents.download_document(id=document_id)
        return res