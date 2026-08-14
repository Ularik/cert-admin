from src.models.tasks import TaskDocuments
from src.repositories.base import BaseRepository
from src.schemas.tasks import TaskDocumentLiteOutSchema, TaskDocumentAddSchema
from sqlalchemy import insert, select


class TasksDocumentRepository(BaseRepository):
    model = TaskDocuments
    schema = TaskDocumentLiteOutSchema

    async def add_documents(
            self,
            tasks_documents_datas: list[TaskDocumentAddSchema]
        ) -> list[TaskDocumentLiteOutSchema]:
        if not tasks_documents_datas:
            return []

        task_id = tasks_documents_datas[0].task_id

        query = select(self.model.filename).where(TaskDocuments.task_id == task_id)
        result = await self.session.execute(query)

        existing_filenames = set(result.scalars().all())

        docs_to_insert = []
        for file_schema in tasks_documents_datas:
            if file_schema.file.filename in existing_filenames:
                continue

            file_bytes = await file_schema.file.read()

            docs_to_insert.append({
                "filename": file_schema.file.filename,
                "mime_type": file_schema.file.content_type or "application/octet-stream",
                "file_data": file_bytes,
                "task_id": task_id,
            })

            existing_filenames.add(file_schema.file.filename)

        if docs_to_insert:
            stmt = (insert(self.model)
                    .values(docs_to_insert)
                    .returning(TaskDocuments.id, TaskDocuments.filename)
                    )
            result = await self.session.execute(stmt)
            return [TaskDocumentLiteOutSchema.model_validate(d) for d in result.all()]

        return []

