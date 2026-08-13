from src.exceptions.exceptions import UniqueObjIsExistException
from src.schemas.users import UserLoginSchema, UserInCookiesSchema, UsersRequestSchema, UserOutSchema, UserAddSchema
from src.services.base import BaseService
from src.services.auth import AuthService
from fastapi import HTTPException


class UserService(BaseService):

    async def login_user(self, data: UserLoginSchema) -> str:
        user = await self.db.users.get_user_with_hashed_pswd(username=data.username, last_name=data.last_name)
        if not user:
            raise HTTPException(status_code=401, detail="Пользователь не найден")
        if not await AuthService().verify_password(data.password, user.hashed_password):
            raise HTTPException(status_code=401, detail="Неверный пароль!")

        payload = UserInCookiesSchema(**{"user_id": user.id, "status": user.status})
        access_token = await AuthService().create_access_token(payload)
        return access_token

    async def create_user(self, data: UsersRequestSchema) -> UserOutSchema:
        hashed_password = await AuthService().hash_pswd(data.password)

        new_data = UserAddSchema(
            username=data.username,
            last_name=data.last_name,
            status=data.status,
            hashed_password=hashed_password,
        )

        try:
            new_user = await self.db.users.add_obj(new_data)
            await self.db.save()
            return new_user
        except UniqueObjIsExistException as err:
            raise HTTPException(status_code=409, detail=err.detail)


    async def get_users(self):
        return await self.db.users.get_objects()