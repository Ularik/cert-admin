from src.repositories.users_repository import UsersRepository
from src.repositories.departments_repository import DepartmentsRepository
from src.repositories.tasks_repository import TasksRepository
from src.repositories.task_document_repository import TasksDocumentRepository
from src.repositories.tasks_users_repository import UsersTasksRepository

class DbManager:
    def __init__(self, session_factory):
        self.session_factory = session_factory

    async def __aenter__(self):
        self.session = self.session_factory()
        self.users = UsersRepository(self.session)
        self.departments = DepartmentsRepository(self.session)
        self.tasks = TasksRepository(self.session)
        self.tasks_documents = TasksDocumentRepository(self.session)
        self.tasks_users = UsersTasksRepository(self.session)
        return self

    async def __aexit__(self, *args):
        await self.session.rollback()
        await self.session.close()

    async def save(self):
        await self.session.commit()