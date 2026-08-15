from src.repositories.base import BaseRepository
from src.models.tasks import TaskReply
from src.schemas.tasks_reply import ReplyCreateSchema, ReplyLiteOutSchema

class ReplyRepository(BaseRepository):
    model = TaskReply
    schema = ReplyLiteOutSchema

    async def create_tasks_reply(self, data: ReplyCreateSchema):
        reply: ReplyLiteOutSchema = await self.add_obj(data)

