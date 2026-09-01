from pydantic import BaseModel, ConfigDict
from src.schemas.users import UserOutSchema
from src.schemas.tasks import DocumentLiteSchema


class ReplyCreateSchema(BaseModel):
    task_id: int
    author_id: int | None = None
    content: str | None = None

class ReplyLiteOutSchema(ReplyCreateSchema):
    id: int
    model_config = ConfigDict(from_attributes=True, extra="ignore")


class ReplyFullOutSchema(ReplyCreateSchema):
    id: int
    author: UserOutSchema | None = None
    attachments: list[DocumentLiteSchema]
    model_config = ConfigDict(from_attributes=True, extra="ignore")


