from advanced_alchemy.repository import SQLAlchemyAsyncRepository
from advanced_alchemy.service import SQLAlchemyAsyncRepositoryService

from app.models import Task


class TaskService(SQLAlchemyAsyncRepositoryService[Task]):
    class Repo(SQLAlchemyAsyncRepository[Task]):
        model_type = Task

    repository_type = Repo
