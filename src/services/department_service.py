from src.exceptions.exceptions import UniqueObjIsExistException, DepartmentAlreadyExistException, \
    ObjectNotFoundException, DepartmentNotFoundException
from src.schemas.users import UserUpdateSchema
from src.services.base import BaseService
from src.schemas.departments import DepartmentCreateUpdateSchema, DepartmentsOutSchema, \
    DepartmentRequestCreateUpdateSchema, DepartmentsWithHeadsOutSchema


class DepartmentService(BaseService):

    async def add_department(self, data: DepartmentRequestCreateUpdateSchema) -> DepartmentsOutSchema:
        new_dep_data = DepartmentCreateUpdateSchema(title=data.title, description=data.description)
        try:
            new_dep: DepartmentsOutSchema = await self.db.departments.add_obj(new_dep_data)
        except UniqueObjIsExistException as err:
            raise DepartmentAlreadyExistException from err

        if data.head_id:
            data = UserUpdateSchema(status="ADMIN", department_id=new_dep.id)
            await self.db.users.update_user(user_id=data.head_id, data=data)
        if data.deputy_head_id:
            data = UserUpdateSchema(status="DEPUTY", department_id=new_dep.id)
            await self.db.users.update_user(user_id=data.head_id, data=data)

        await self.db.save()
        return new_dep

    async def update_department(self, dep_id: int, data: DepartmentRequestCreateUpdateSchema) -> DepartmentsOutSchema:
        new_dep_data = DepartmentCreateUpdateSchema(title=data.title, description=data.description)
        try:
            old_department: DepartmentsWithHeadsOutSchema = await self.get_one_department(department_id=dep_id)
            new_department: DepartmentsOutSchema = await self.db.departments.edit(new_dep_data, id=dep_id, exclude_unset=True)
        except UniqueObjIsExistException as err:
            raise DepartmentAlreadyExistException from err
        except ObjectNotFoundException as err:
            raise DepartmentNotFoundException from err

        old_heads = set()
        if old_department.head:
            old_heads.add(old_department.head.id)
        if old_department.deputy_head:
            old_heads.add(old_department.deputy_head.id)

        new_heads = set(filter(None, [data.head_id, data.deputy_head_id]))

        old_heads_for_set_status_to_user = old_heads - new_heads

        if old_heads_for_set_status_to_user:
            await self.db.users.update_status(users_ids=old_heads_for_set_status_to_user, status="USER")

        if data.head_id and data.head_id not in old_heads:
            update_users_data = UserUpdateSchema(department_id=new_department.id, status="HEAD")
            await self.db.users.update_user(data=update_users_data, user_id=data.head_id)
        if data.deputy_head_id and data.deputy_head_id not in old_heads:
            update_users_data = UserUpdateSchema(department_id=new_department.id, status="DEPUTY")
            await self.db.users.update_user(data=update_users_data, user_id=data.deputy_head_id)

        await self.db.save()
        return new_department

    async def get_department(self) -> list[DepartmentsWithHeadsOutSchema]:
        return await self.db.departments.get_departments()

    async def get_one_department(self, department_id: int) -> DepartmentsWithHeadsOutSchema:
        res: list[DepartmentsWithHeadsOutSchema] = await self.db.departments.get_departments(id=department_id)
        if not res:
            raise DepartmentNotFoundException
        return res[0]