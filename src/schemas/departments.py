from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime


class DepartmentCreateSchema(BaseModel):
    title: str = Field(description="Название отдела")
    description: str | None = Field(description="Описание отдела", default=None)


class DepartmentsOutSchema(DepartmentCreateSchema):
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)