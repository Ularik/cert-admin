from src.exceptions.exceptions import UniqueObjIsExistException, DepartmentAlreadyExistException
from src.services.base import BaseService
from src.schemas.departments import DepartmentCreateSchema, DepartmentsOutSchema

class DepartmentService(BaseService):

    async def add_department(self, data: DepartmentCreateSchema) -> DepartmentsOutSchema:
        try:
            res = await self.db.departments.add_obj(data)
        except UniqueObjIsExistException as err:
            raise DepartmentAlreadyExistException
        await self.db.save()
        return res

    async def get_department(self) -> list[DepartmentsOutSchema]:
        return await self.db.departments.get_objects()