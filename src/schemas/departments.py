from datetime import datetime
from pydantic import BaseModel, Field, model_validator, ConfigDict


class DepartmentCreateUpdateSchema(BaseModel):
    title: str = Field(description="Название отдела")
    description: str | None = Field(description="Описание отдела", default=None)
    head_id: int | None = Field(default=None, description="ID руководителя")
    deputy_head_id: int | None = Field(default=None, description="ID заместителя")

    @model_validator(mode="after")
    def validate_head_and_deputy_different(self) -> "DepartmentCreateUpdateSchema":
        if (
            self.head_id is not None
            and self.deputy_head_id is not None
            and self.head_id == self.deputy_head_id
        ):
            raise ValueError(
                "Начальник и заместитель начальника не могут быть одним и тем же человеком."
            )
        return self


class DepartmentLiteOutSchema(BaseModel):
    id: int
    title: str
    model_config = ConfigDict(from_attributes=True, extra="ignore")

class DepartmentsOutSchema(DepartmentCreateUpdateSchema):
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)