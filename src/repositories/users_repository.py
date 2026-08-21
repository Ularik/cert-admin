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

    async def update_user(self, data: UserUpdateSchema, user_id: int) -> UserOutSchema:
        res: UserOutSchema = await self.edit(data, id=user_id)
        return res

    async def update_status(self, users_ids: list[int], status: Literal["ADMIN", "HEAD", "USER"]):
        query = (
            update(self.model)
            .filter(self.model.id.in_(users_ids))
            .values(status=status)
            .returning(self.model)
        )
        await self.session.execute(query)

    async def get_user_full_data(self, department_id: int = None) -> list[UserWithDepartmentOut]:

        query = (
            select(
                self.model.id,
                self.model.username,
                self.model.last_name,
                self.model.status,
                self.model.department_id,
                Departments.title.label("department_title"),
            )
            .outerjoin(Departments, self.model.department_id == Departments.id)
        )

        if department_id:
            query = query.where(self.model.department == department_id)

        result = await self.session.execute(query)
        return [UserWithDepartmentOut.model_validate(u) for u in result.mappings().all()]