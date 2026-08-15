from fastapi import UploadFile

from src.models.tasks import TaskDocuments
from src.repositories.base import BaseRepository
from src.schemas.tasks import DocumentLiteSchema
from sqlalchemy import insert, select


class TasksDocumentRepository(BaseRepository):
    model = TaskDocuments
    schema = DocumentLiteSchema

    async def get_existing_filenames(
            self,
            **kwargs
    ) -> set[str]:
        query = select(self.model.filename).filter_by(**kwargs)
        result = await self.session.execute(query)

        existing_filenames = set(result.scalars().all())
        return existing_filenames

    async def add_documents(
            self,
            documents_files: list[UploadFile],
            **kwargs
        ) -> list[DocumentLiteSchema]:
        if not documents_files:
            return []

        existing_filenames: set[str] = await self.get_existing_filenames(**kwargs)

        docs_to_insert = []
        for file in documents_files:
            if file.filename in existing_filenames:
                continue

            file_bytes = await file.read()
            docs_to_insert.append({
                "filename": file.filename,
                "mime_type": file.content_type or "application/octet-stream",
                "file_data": file_bytes,
                **kwargs,
            })

            existing_filenames.add(file.filename)

        if docs_to_insert:
            stmt = (insert(self.model)
                    .values(docs_to_insert)
                    .returning(self.model.id, self.model.filename)
                    )
            result = await self.session.execute(stmt)
            return [self.schema.model_validate(d) for d in result.all()]

        return []

    async def update_documents(
            self,
            old_docs_id_from_front: list[DocumentLiteSchema],
            new_documents: list[UploadFile],
            **kwargs
    ) -> list[DocumentLiteSchema]:
        actual_old_docs: list[DocumentLiteSchema] = await self.get_filtered_objects(**kwargs)

        delete_old_docs = (
                set(map(lambda x: x.id, actual_old_docs))
                -
                set(old_docs_id_from_front)
        )
        if delete_old_docs:
            filter = self.model.id.in_(delete_old_docs)
            await self.delete_bulk(filter, **kwargs)

        return await self.add_documents(new_documents)