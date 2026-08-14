from pydantic import BaseModel, ConfigDict
from fastapi import UploadFile
from datetime import datetime
from src.schemas.users import UserOutSchema


class TaskDocumentAddSchema(BaseModel):
    file: UploadFile
    task_id: int


class TaskDocumentOutSchema(TaskDocumentAddSchema):
    id: int
    model_config = ConfigDict(from_attributes=True, extra="ignore")


class TaskDocumentLiteOutSchema(BaseModel):
    id: int
    filename: str
    model_config = ConfigDict(from_attributes=True, extra="ignore")


class TaskCreateUpdateSchema(BaseModel):
    author_id: int
    title: str
    description: str | None = None
    department_id: int | None = None
    model_config = ConfigDict(from_attributes=True, extra="ignore")


class TaskLiteOutSchema(TaskCreateUpdateSchema):
    id: int
    created_at: datetime
    updated_at: datetime

class TaskOutSchema(TaskCreateUpdateSchema):
    id: int
    executors: list[UserOutSchema]
    attachments: list[TaskDocumentLiteOutSchema]
    created_at: datetime
    updated_at: datetime

# class Task

