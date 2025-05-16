from uuid import UUID

from pydantic import BaseModel


class TaskCreate(BaseModel):
    title: str
    description: str | None = None


class TaskUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    completed: bool | None = None


class TaskOut(BaseModel):
    id: int
    title: str
    description: str | None
    completed: bool

    class Config:
        from_attributes = True


class CeleryTaskCreate(BaseModel):
    task_id: UUID


class CeleryTaskResult(BaseModel):
    progress: int
    state: str | None
