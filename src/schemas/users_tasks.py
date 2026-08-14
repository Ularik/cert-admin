from pydantic import BaseModel


class UsersConnectTaskSchema(BaseModel):
    user_id: int
    tasks_id: int
