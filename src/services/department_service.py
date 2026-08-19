from src.exceptions.exceptions import UniqueObjIsExistException, DepartmentAlreadyExistException, \
    ObjectNotFoundException, DepartmentNotFoundException
from src.schemas.users import UserUpdateSchema
from src.services.base import BaseService
from src.schemas.departments import DepartmentCreateUpdateSchema, DepartmentsOutSchema

class DepartmentService(BaseService):

    async def add_department(self, data: DepartmentCreateUpdateSchema) -> DepartmentsOutSchema:
        try:
            res = await self.db.departments.add_obj(data)
        except UniqueObjIsExistException as err:
            raise DepartmentAlreadyExistException

        heads = list(filter(None, [data.head_id, data.deputy_head_id]))

        if heads:
            await self.db.users.update_status(users_ids=heads, status="HEAD")

        await self.db.save()
        return res

    async def update_department(self, dep_id: int, data: DepartmentCreateUpdateSchema) -> DepartmentsOutSchema:
        try:
            old_department: DepartmentsOutSchema = await self.db.departments.get_one(id=dep_id)
            new_department: DepartmentsOutSchema = await self.db.departments.edit(data, id=dep_id, exclude_unset=True)
        except UniqueObjIsExistException as err:
            raise DepartmentAlreadyExistException
        except ObjectNotFoundException:
            raise DepartmentNotFoundException

        old_heads = set(filter(None, [old_department.head_id, old_department.deputy_head_id]))
        new_heads = set(filter(None, [new_department.head_id, new_department.deputy_head_id]))

        old_heads = old_heads - new_heads
        new_heads = new_heads - old_heads

        if old_heads:
            await self.db.users.update_status(users_ids=old_heads, status="USER")
        if new_heads:
            update_users_data = UserUpdateSchema(department=new_department.id, status="HEAD")
            await self.db.users.update_users_bulk(data=update_users_data, users_ids=new_heads)

        await self.db.save()
        return new_department

    async def get_department(self) -> list[DepartmentsOutSchema]:
        return await self.db.departments.get_objects()

    async def get_one_department(self, department_id: int) -> DepartmentsOutSchema:
        try:
            res: DepartmentsOutSchema = await self.db.departments.get_one(id=department_id)
        except ObjectNotFoundException:
            raise DepartmentNotFoundException
        return res