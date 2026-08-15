from pydantic import BaseModel, ConfigDict
from fastapi import UploadFile
from src.schemas.tasks import DocumentLiteSchema


class ReplyCreateSchema(BaseModel):
    task_id: int
    content: str | None = None

class ReplyLiteOutSchema(ReplyCreateSchema):
    id: int
    model_config = ConfigDict(from_attributes=True, extra="ignore")

class ReplyDocumentAddSchema(BaseModel):
    file: UploadFile
    reply_id: int


class ReplyFullOutSchema(ReplyCreateSchema):
    id: int
    attachments: list[DocumentLiteSchema]


