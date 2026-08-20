from src.models import Departments
from src.repositories.base import BaseRepository
from src.models.users import Users
from src.models.users_tasks import UsersTasks
from src.schemas.users import UserHashedPswdSchema, UserOutSchema, UserWithDepartmentOut, UserUpdateSchema
from src.schemas.users_tasks import UsersConnectTaskSchema
from sqlalchemy import select, insert, update
from sqlalchemy.orm import aliased
from typing import Literal


class UsersRepository(BaseRepository):
    model = Users
    schema = UserOutSchema

    async def get_user_with_hashed_pswd(self, username: str, last_name: str) -> UserHashedPswdSchema:
        query = select(self.model).filter_by(username=username, last_name=last_name)
        result = await self.session.execute(query)
        user = result.scalars().first()
        if user:
            return UserHashedPswdSchema.model_validate(user)

    async def relate_users_tasks(self, data: UsersConnectTaskSchema):
        await self.session.execute(
            insert(UsersTasks)
            .values(**data.model_dump())
        )

    async def update_status(self, users_ids: list[int], status: Literal["ADMIN", "HEAD", "USER"]):
        query = (
            update(self.model)
            .filter(self.model.id.in_(users_ids))
            .values(status=status)
            .returning(self.model)
        )
        await self.session.execute(query)

    async def update_department(self, users_ids: list[int], new_department_id: int):
        query = (
            update(self.model)
             .values(department=new_department_id)
             .filter(self.model.id.in_(users_ids))
            )
        await self.session.execute(query)

    async def update_users_bulk(self, data: UserUpdateSchema, users_ids: list[int]):
        filters = self.model.id.in_(users_ids)
        return await self.edit_bulk(data, filters)

    async def get_user_full_data(self, department_id: int = None) -> list[UserWithDepartmentOut]:
        # Используем aliased, чтобы чётко разграничить JOIN-ы
        DeptMember = aliased(Departments, name="dept_member")
        DeptHead = aliased(Departments, name="dept_head")
        DeptDeputy = aliased(Departments, name="dept_deputy")

        query = (
            select(
                self.model.id,
                self.model.username,
                self.model.last_name,
                self.model.status,
                DeptMember.id.label("department_id"),
                DeptMember.title.label("member_department"),
                DeptHead.title.label("head_of_department"),
                DeptDeputy.title.label("deputy_head_of_department"),
            )
            .outerjoin(DeptMember, self.model.department == DeptMember.id)
            .outerjoin(DeptHead, self.model.id == DeptHead.head_id)
            .outerjoin(DeptDeputy, self.model.id == DeptDeputy.deputy_head_id)
        )

        if department_id:
            query = query.where(self.model.department == department_id)

        result = await self.session.execute(query)
        return [UserWithDepartmentOut.model_validate(u) for u in result.mappings().all()]