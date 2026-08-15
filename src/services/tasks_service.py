from src.exceptions.exceptions import ObjectNotFoundException, DepartmentNotFoundException, UniqueObjIsExistException, \
    TaskAlreadyExistException
from src.routers.dependencies import QueryParamsSchema
from src.schemas.users_tasks import UsersConnectTaskSchema
from src.services.base import BaseService
from src.schemas.tasks import (TaskCreateUpdateSchema, TaskOutSchema,
                               TaskLiteOutSchema, TaskDocumentAddSchema)
from fastapi import UploadFile
from src.models.users import Users


class TasksService(BaseService):

    async def create_task(
            self,
            user_id: int,
            title: str,
            description: str | None,
            department_id: int | None,
            attachments: list[UploadFile] | None,
            executor_ids: list[int] = []
    ) -> TaskOutSchema:

        task_data = TaskCreateUpdateSchema(author_id=user_id, title=title, description=description, department_id=department_id)
        try:
            new_task: TaskLiteOutSchema = await self.db.tasks.add_obj(task_data)
        except ObjectNotFoundException:
            raise DepartmentNotFoundException
        except UniqueObjIsExistException:
            raise TaskAlreadyExistException

        documents = await self.db.tasks_documents.add_documents(task_id=new_task.id, documents_files=set(attachments or []))
        executors = await self.db.users.get_filtered_objects(Users.id.in_(executor_ids))

        tasks_executors_data_list = [
            UsersConnectTaskSchema(user_id=user_id, task_id=new_task.id)
            for user_id in executor_ids
        ]
        await self.db.tasks_users.connect_user_task(tasks_executors_data_list)
        await self.db.save()

        new_task_full_out = TaskOutSchema(**new_task.model_dump(), attachments=documents, executors=executors)
        return new_task_full_out


    async def update_task(
            self,
            user_id: int,
            task_id: int,
            title: str,
            description: str | None,
            department_id: int | None,
            attachments: list[UploadFile] | None,
            old_attachments_id_from_front: list[int],
            executor_ids: list[int] = []
    ):
        task_data = TaskCreateUpdateSchema(author_id=user_id, title=title, description=description, department_id=department_id)

        task = await self.db.tasks.edit(task_data, exclude_unset=True, id=task_id)

        await self.update_executors_task(executor_ids=executor_ids, task_id=task_id)

        tasks_docs = await self.db.tasks_documents.update_documents(
            task_id=task_id,
            old_docs_id_from_front=old_attachments_id_from_front,
            new_documents=attachments or []
        )
        executors = await self.db.users.get_filtered_objects(Users.id.in_(executor_ids))
        new_task_full_out = TaskOutSchema(**task.model_dump(), attachments=tasks_docs, executors=executors)
        return new_task_full_out


    async def get_tasks(self, query_params: QueryParamsSchema) -> list[TaskOutSchema]:
        tasks: list[TaskOutSchema] = await self.db.tasks.get_filtered_tasks(limit=query_params.limit,
                                                                                  offset=query_params.offset)
        return tasks

    async def update_executors_task(self, executor_ids: list[int], task_id: int) -> None:
        await self.db.tasks_users.set_user_task(executors_ids=executor_ids, task_id=task_id)
