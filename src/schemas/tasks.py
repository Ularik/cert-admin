from pydantic import BaseModel, ConfigDict
from datetime import datetime
from src.schemas.users import UserOutSchema


class TaskDocumentAddSchema(BaseModel):
    filename: str
    mime_type: str
    file_data: bytes
    task_id: int


class TaskDocumentOutSchema(TaskDocumentAddSchema):
    id: int
    model_config = ConfigDict(from_attributes=True, extra="ignore")


class TaskDocumentLiteOutSchema(BaseModel):
    id: int
    filename: str
    model_config = ConfigDict(from_attributes=True, extra="ignore")


class TaskCreateUpdateSchema(BaseModel):
    title: str
    description: str | None = None
    department_id: int | None = None
    model_config = ConfigDict(from_attributes=True, extra="ignore")


class TaskLiteOutSchema(TaskCreateUpdateSchema):
    id: int

class TaskOutSchema(TaskCreateUpdateSchema):
    id: int
    executors: list[UserOutSchema]
    attachments: list[TaskDocumentLiteOutSchema]
    created_at: datetime
    updated_at: datetime

