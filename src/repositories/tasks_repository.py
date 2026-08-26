from src.models.departments_tasks import DepartmentsTasks
from src.models.departments import Departments
from src.models.tasks import Tasks
from src.repositories.base import BaseRepository
from src.schemas.tasks import TaskLiteOutSchema, TaskFullOutSchema, TaskApiResponseSchema
from sqlalchemy import select, func
from sqlalchemy.orm import selectinload, joinedload


class TasksRepository(BaseRepository):
    model = Tasks
    schema = TaskLiteOutSchema

    async def get_filtered_tasks(self, limit: int = 10, offset: int = 0, *args, **kwargs) -> TaskApiResponseSchema:
        base_query = select(self.model).filter(*args).filter_by(**kwargs)

        # 1. Подсчет количества через subquery
        count_query = select(func.count()).select_from(base_query.order_by(None).subquery())
        total_count = (await self.session.execute(count_query)).scalar_one()

        # 2. Добавление связей и пагинации
        data_query = (
            base_query
            .options(
                joinedload(self.model.author),
                selectinload(self.model.attachments),
                selectinload(self.model.departments),
                selectinload(self.model.executors)
            )
            .order_by(self.model.created_at.desc())
            .limit(limit)
            .offset(offset)
        )
        result = await self.session.execute(data_query)
        items = [TaskFullOutSchema.model_validate(row) for row in result.scalars()]

        return TaskApiResponseSchema(total=total_count, items=items)

    async def get_task_department_ids(self, task_id: int) -> list[int]:
        query = select(DepartmentsTasks.department_id).where(
            DepartmentsTasks.task_id == task_id
        )
        res = await self.session.execute(query)
        return list(res.scalars().all())



