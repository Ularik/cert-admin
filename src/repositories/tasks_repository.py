from src.models.tasks import Tasks, TaskDocuments
from src.repositories.base import BaseRepository
from src.schemas.tasks import TaskCreateUpdateSchema, TaskOutSchema, TaskLiteOutSchema, TaskDocumentLiteOutSchema
from fastapi import UploadFile
from sqlalchemy import insert, select
from src.models.tasks import TaskDocuments


class TasksRepository(BaseRepository):
    model = Tasks
    schema = TaskLiteOutSchema

    async def add_documents(
            self,
            task_id: int,
            attachments: list[UploadFile]
        ) -> list[TaskDocumentLiteOutSchema]:

        query = select(TaskDocuments.filename).where(TaskDocuments.task_id == task_id)
        result = await self.session.execute(query)

        existing_filenames = set(result.scalars().all())

        docs_to_insert = []
        for file in attachments:
            if file.filename in existing_filenames:
                continue

            file_bytes = await file.read()

            docs_to_insert.append({
                "filename": file.filename,
                "mime_type": file.content_type or "application/octet-stream",
                "file_data": file_bytes,
                "task_id": task_id,
            })

            existing_filenames.add(file.filename)

        if docs_to_insert:
            stmt = (insert(TaskDocuments)
                    .values(docs_to_insert)
                    .returning(TaskDocuments.id, TaskDocuments.filename)
                    )
            result = await self.session.execute(stmt)
            return [TaskDocumentLiteOutSchema.model_validate(d) for d in result.all()]

        return []

