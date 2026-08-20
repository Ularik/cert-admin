from src.schemas.users import UserInCookiesSchema
from src.schemas.users_tasks import UsersConnectTaskSchema
from src.schemas.tasks_reply import ReplyLiteOutSchema
from src.services.base import BaseService
from fastapi import UploadFile
from src.schemas.tasks_reply import ReplyCreateSchema, ReplyFullOutSchema
from src.schemas.tasks import DocumentLiteSchema

class ReplyService(BaseService):

    async def create_reply(
            self,
            executor: UserInCookiesSchema,
            task_id: int,
            content: str,
            attachments: list[UploadFile]
    ):
        await self.db.tasks_users.connect_user_task(task_id=task_id, executor_ids=[executor.user_id])

        reply_data = ReplyCreateSchema(task_id=task_id, content=content)
        reply: ReplyLiteOutSchema = await self.db.reply_tasks.add_obj(reply_data)

        documents: list[DocumentLiteSchema] = await self.db.reply_documents.add_documents(
            documents_files=attachments,
            reply_id=reply.id
        )
        reply_with_docs = ReplyFullOutSchema(**reply.model_dump(), attachments=documents)
        await self.db.save()
        return reply_with_docs

