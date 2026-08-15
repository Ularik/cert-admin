from src.repositories.task_document_repository import TasksDocumentRepository
from src.models.tasks import ReplyDocument
from src.schemas.tasks import DocumentLiteSchema


class ReplyDocumentsRepository(TasksDocumentRepository):
    model = ReplyDocument
    schema = DocumentLiteSchema

