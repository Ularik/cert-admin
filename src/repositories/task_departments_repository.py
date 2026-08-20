from src.models.departments_tasks import DepartmentsTasks
from src.schemas.departments_tasks import DepartmentsConnectTaskSchema
from src.repositories.base import BaseRepository


class DepartmentsTasksRepository(BaseRepository):
    model = DepartmentsTasks
    schema = DepartmentsConnectTaskSchema

    async def connect_departments_to_task(self, task_id: int, departments_ids: list[int]):
        tasks_departments_data_list = [
            self.schema(department_id=dep_id, task_id=task_id)
            for dep_id in departments_ids
        ]
        await super().add_bulk(tasks_departments_data_list)