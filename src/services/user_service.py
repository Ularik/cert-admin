from src.exceptions.exceptions import UniqueObjIsExistException, UserAlreadyExistException
from src.schemas.users import UserLoginSchema, UserInCookiesSchema, UsersAuthSchema, UserOutSchema, UserAddSchema, \
    UserUpdateSchema
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

    async def set_department(self, user_id: int, department_id: int) -> UserOutSchema:
        data = UserUpdateSchema(department_id=department_id)
        user = await self.db.users.edit(data, exclude_unset=True, id=user_id)
        await self.db.save()
        return user

    async def create_user(self, data: UsersAuthSchema) -> UserOutSchema:
        hashed_password = await AuthService().hash_pswd(data.password)

        new_data = UserAddSchema(
            username=data.username,
            last_name=data.last_name,
            status=data.status,
            department_id=data.department_id,
            hashed_password=hashed_password,
        )

        try:
            new_user = await self.db.users.add_obj(new_data)
            await self.db.save()
            return new_user
        except UniqueObjIsExistException as err:
            raise HTTPException(status_code=409, detail=err.detail)

    async def get_user(self, id: int) -> UserOutSchema:
        return await self.db.users.get_one(id=id)

    async def get_users(self, department_id: int = None):
        return await self.db.users.get_user_full_data(department_id=department_id)

    async def update_user(self, data: UserUpdateSchema, user_id: int) -> UserOutSchema:
        try:
            new_user = await self.db.users.update_user(data=data, user_id=user_id)
        except UniqueObjIsExistException as err:
            raise UserAlreadyExistException from err

        await self.db.save()
        return new_user

    async def delete_user(self, user_id: int) -> None:
        await self.db.users.delete_bulk(id=user_id)
        await self.db.save()