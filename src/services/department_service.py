from src.exceptions.exceptions import UniqueObjIsExistException, DepartmentAlreadyExistException
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
            res: DepartmentsOutSchema = await self.db.departments.edit(data, id=dep_id, exclude_unset=True)
        except UniqueObjIsExistException as err:
            raise DepartmentAlreadyExistException

        heads = []
        if res.head_id != data.head_id and data.head_id is not None:
            heads.append(data.head_id)
        if res.deputy_head_id != data.deputy_head_id and data.deputy_head_id is not None:
            heads.append(data.deputy_head_id)

        if heads:
            await self.db.users.update_status(users_ids=heads, status="HEAD")

        await self.db.save()
        return res

    async def get_department(self) -> list[DepartmentsOutSchema]:
        return await self.db.departments.get_objects()