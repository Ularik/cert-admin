from src.repositories.base import BaseRepository
from src.models.users import Users, UsersTasks
from src.schemas.users import UserHashedPswdSchema, UserOutSchema, UsersTasksSchema
from sqlalchemy import select, insert


class UsersRepository(BaseRepository):
    model = Users
    schema = UserOutSchema

    async def get_user_with_hashed_pswd(self, username: str, last_name: str) -> UserHashedPswdSchema:
        query = select(self.model).filter_by(username=username, last_name=last_name)
        result = await self.session.execute(query)
        user = result.scalars().first()
        if user:
            return UserHashedPswdSchema.model_validate(user)

    async def relate_users_tasks(self, data: UsersTasksSchema):
        await self.session.execute(
            insert(UsersTasks)
            .values(**data.model_dump())
        )