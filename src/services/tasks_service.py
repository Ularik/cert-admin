from src.schemas.users import UsersTasksSchema
from src.services.base import BaseService
from src.schemas.tasks import TaskCreateUpdateSchema, TaskOutSchema, TaskLiteOutSchema
from fastapi import UploadFile
from src.repositories.users_repository import UsersRepository


class TasksService(BaseService):

    async def create_task(
            self,
            title: str,
            description: str | None,
            department_id: int | None,
            attachments: list[UploadFile],
            executor_ids: list[int] | None
    ):
        task_data = TaskCreateUpdateSchema(title=title, description=description, department_id=department_id)
        new_task: TaskLiteOutSchema = await self.db.tasks.add_obj(task_data)
        attachments = await self.db.tasks.add_documents(task=new_task, attachments=attachments)

        # data = UsersTasksSchema(user_id=user_id, task_id=task_id)
        # executors = await UsersRepository(self.db.session).create_users_tasks()

        await self.db.save()

        TaskOutSchema(**new_task.model_dump(), attachments=attachments)
        return new_task


    async def update_task(self, task_id: int, data: TaskCreateUpdateSchema, attachments: list[UploadFile]):
        task = await self.db.tasks.edit(data, exclude_unset=True, id=task_id)
        await self.db.tasks.add_documents(task=task, attachments=attachments)
        return task