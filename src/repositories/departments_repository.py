from src.repositories.base import BaseRepository
from src.models.departments import Departments
from src.schemas.departments import DepartmentsOutSchema, DepartmentCreateSchema


class DepartmentsRepository(BaseRepository):
    model = Departments
    schema = DepartmentsOutSchema


