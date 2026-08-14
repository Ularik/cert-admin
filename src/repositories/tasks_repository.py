from src.models.tasks import Tasks, TaskDocuments
from src.repositories.base import BaseRepository
from src.schemas.tasks import TaskLiteOutSchema, TaskOutSchema
from sqlalchemy import select
from sqlalchemy.orm import selectinload



class TasksRepository(BaseRepository):
    model = Tasks
    schema = TaskLiteOutSchema

    async def get_filtered_tasks(self, limit: int = 10, offset: int = 0, *args, **kwargs) -> list[TaskOutSchema]:
        query = (
            select(self.model)
            .options(
                selectinload(Tasks.attachments),
                selectinload(Tasks.executors)
            )
            .filter(*args)
            .filter_by(**kwargs)
            .limit(limit)
            .offset(offset)
        )

        result = await self.session.execute(query)
        return [TaskOutSchema.model_validate(row) for row in result.scalars()]



