from src.exceptions.exceptions import ObjectNotFoundException, DepartmentNotFoundException, UniqueObjIsExistException, \
    TaskAlreadyExistException, HasNotRightsToTaskException, UserNotFoundException, DependsDepartmentException, \
    TaskNotFoundException, HasNoRightsToUpdateDepartment
from src.routers.dependencies import QueryParamsSchema
from src.schemas.departments_tasks import DepartmentsConnectTaskSchema
from src.schemas.users import UserOutSchema, UserInCookiesSchema
from src.schemas.users_tasks import UsersConnectTaskSchema
from src.services.base import BaseService
from src.schemas.tasks import (TaskCreateUpdateSchema, TaskOutSchema,
                               TaskLiteOutSchema, TaskApiResponseSchema, TaskFullOutSchema)
from fastapi import UploadFile
from src.models.users import Users


class TasksService(BaseService):

    async def create_admin_task(
            self,
            user: UserInCookiesSchema,
            title: str,
            description: str | None,
            attachments: list[UploadFile] | None,
            departments_ids: list[int] = [],
            executor_ids: list[int] = []
    ):
        if user.status != "ADMIN":
            raise HasNoRightsToUpdateDepartment

        task_data = TaskCreateUpdateSchema(author_id=user.user_id, title=title, description=description)
        try:
            new_task: TaskLiteOutSchema = await self.db.tasks.add_obj(task_data)
        except UniqueObjIsExistException:
            raise TaskAlreadyExistException

        documents = await self.db.tasks_documents.add_documents(documents_files=set(attachments or []), task_id=new_task.id, )

        try:
            await self.db.tasks_users.connect_user_task(task_id=new_task.id, executor_ids=executor_ids)
        except ObjectNotFoundException:
            raise UserNotFoundException

        try:
            await self.db.task_departments.connect_departments_to_task(task_id=new_task.id, departments_ids=departments_ids)
        except ObjectNotFoundException:
            raise DepartmentNotFoundException

        await self.db.save()

        new_task_full_out = TaskOutSchema(**new_task.model_dump(), attachments=documents, executors=executor_ids)
        return new_task_full_out


    async def create_task(
            self,
            user_id: int,
            title: str,
            description: str | None,
            attachments: list[UploadFile] | None,
            departments_ids: list[int] = [],
            executor_ids: list[int] = []
    ) -> TaskOutSchema:

        user: UserOutSchema = await self.db.users.get_one(id=user_id)

        if user.status != "ADMIN" and not user.department_id:
            raise DependsDepartmentException

        if user.status != "ADMIN":
            departments_ids = [user.department_id]

        task_data = TaskCreateUpdateSchema(author_id=user_id, title=title, description=description)
        try:
            new_task: TaskLiteOutSchema = await self.db.tasks.add_obj(task_data)
        except UniqueObjIsExistException:
            raise TaskAlreadyExistException

        documents = await self.db.tasks_documents.add_documents(task_id=new_task.id, documents_files=set(attachments or []))

        try:
            await self.db.tasks_users.connect_user_task(task_id=new_task.id, executor_ids=executor_ids)
        except ObjectNotFoundException:
            raise UserNotFoundException

        try:
            await self.db.task_departments.connect_departments_to_task(task_id=new_task.id, departments_ids=departments_ids)
        except ObjectNotFoundException:
            raise DepartmentNotFoundException

        await self.db.save()

        new_task_full_out = TaskOutSchema(**new_task.model_dump(), attachments=documents, executors=executor_ids)
        return new_task_full_out


    async def update_task(
            self,
            user_id: int,
            task_id: int,
            title: str,
            description: str | None,
            attachments: list[UploadFile] | None,
            old_attachments_id_from_front: list[int],
            departments_ids: list[int] = [],
            executor_ids: list[int] = []
    ):
        user: UserOutSchema = await self.db.users.get_one(id=user_id)

        if user.status != "ADMIN":
            if not user.department_id:
                raise HasNotRightsToTaskException

            old_departments_ids = await self.db.tasks.get_task_department_ids(task_id=task_id)
            if old_departments_ids != [user.department_id]:
                raise HasNotRightsToTaskException

        task_data = TaskCreateUpdateSchema(author_id=user_id, title=title, description=description)
        try:
            task = await self.db.tasks.edit(task_data, exclude_unset=True, id=task_id)
        except ObjectNotFoundException:
            raise DepartmentNotFoundException

        await self.update_executors_task(executor_ids=executor_ids, task_id=task_id)

        tasks_docs = await self.db.tasks_documents.update_documents(
            task_id=task_id,
            old_docs_id_from_front=old_attachments_id_from_front,
            new_documents=attachments or []
        )
        await self.db.task_departments.connect_departments_to_task(task_id=task_id, departments_ids=departments_ids)

        new_task_full_out = TaskOutSchema(**task.model_dump(), attachments=tasks_docs, executors=executor_ids)
        await self.db.save()
        return new_task_full_out


    async def get_tasks(self, query_params: QueryParamsSchema) -> TaskApiResponseSchema:
        resp: TaskApiResponseSchema = await self.db.tasks.get_filtered_tasks(limit=query_params.limit,
                                                                                  offset=query_params.offset)
        return resp

    async def get_one(self, task_id: int) -> TaskFullOutSchema:
        task: TaskApiResponseSchema = await self.db.tasks.get_filtered_tasks(id=task_id)
        if not task.items:
            raise TaskNotFoundException
        return task.items[0]

    async def update_executors_task(self, executor_ids: list[int], task_id: int) -> None:
        await self.db.tasks_users.set_user_task(executors_ids=executor_ids, task_id=task_id)

    async def delete_task(self, task_id: int, user_id: int) -> None:
        task: TaskLiteOutSchema = await self.db.tasks.get_one(id=task_id)
        if task.author_id != user_id:
            raise HasNotRightsToTaskException
        await self.db.tasks.delete_bulk(id=task_id)
        await self.db.save()

    async def delete_task_by_head(self, task_id: int, user_id: int):
        user: UserOutSchema  = await self.db.users.get_one(id=user_id)
        departments_ids = await self.db.tasks.get_task_department_ids(task_id=task_id)
        if departments_ids != [user.department_id]:
            raise HasNotRightsToTaskException
        await self.db.tasks.delete_bulk(id=task_id)
        await self.db.save()

    async def delete_task_by_admin(self, task_id: int) -> None:
        await self.db.tasks.delete_bulk(id=task_id)
        await self.db.save()