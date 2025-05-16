from typing import Annotated
from uuid import UUID

from advanced_alchemy.exceptions import NotFoundError
from advanced_alchemy.extensions.fastapi import (
    AdvancedAlchemy,
    service,
)
from celery.result import AsyncResult
from fastapi import Depends, FastAPI

from app.database import sqlalchemy_config
from app.exception_handlers import not_found_exception_handler
from app.schemas import CeleryTaskCreate, CeleryTaskResult, TaskCreate, TaskOut, TaskUpdate
from app.service import TaskService
from app.worker import create_long_task

app = FastAPI()
app.add_exception_handler(NotFoundError, not_found_exception_handler)
alchemy = AdvancedAlchemy(config=sqlalchemy_config, app=app)


@app.post('/tasks', response_model=TaskOut)
async def create_task(
    task_service: Annotated[TaskService, Depends(alchemy.provide_service(TaskService))],
    data: TaskCreate,
) -> TaskOut:
    task = await task_service.create(data)
    return task_service.to_schema(task, schema_type=TaskOut)


@app.get(path='/tasks', response_model=service.OffsetPagination[TaskOut])
async def list_authors(
    task_service: Annotated[TaskService, Depends(alchemy.provide_service(TaskService))],
):
    results = await task_service.list()
    return task_service.to_schema(results, schema_type=TaskOut)


@app.put(path='/tasks/{task_id}', response_model=TaskOut)
async def update_author(
    task_service: Annotated[TaskService, Depends(alchemy.provide_service(TaskService))],
    data: TaskUpdate,
    task_id: int,
) -> TaskOut:
    task = await task_service.update(data, item_id=task_id)
    return task_service.to_schema(task, schema_type=TaskOut)


@app.delete(path='/tasks/{task_id}')
async def delete_author(
    task_service: Annotated[TaskService, Depends(alchemy.provide_service(TaskService))],
    task_id: int,
) -> None:
    await task_service.delete(task_id)


@app.post('/long-task', response_model=CeleryTaskCreate)
async def start_long_task():
    task = create_long_task.delay()
    return {'task_id': task.id}


@app.get('/long-task/{task_id}/progress', response_model=CeleryTaskResult)
async def get_long_task_progress(task_id: UUID):
    task_result = AsyncResult(str(task_id))
    if task_result.state == 'PROGRESS':
        return {'progress': task_result.info.get('progress', 0)}
    elif task_result.state == 'SUCCESS':
        return {'progress': 100}
    else:
        return {'progress': 0, 'state': task_result.state}
