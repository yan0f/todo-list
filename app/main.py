from typing import Annotated
from uuid import uuid4

from advanced_alchemy.exceptions import NotFoundError
from advanced_alchemy.extensions.fastapi import (
    AdvancedAlchemy,
    service,
)
from fastapi import BackgroundTasks, Depends, FastAPI

from app import background_tasks as background_tasks_
from app.database import sqlalchemy_config
from app.exception_handlers import not_found_exception_handler
from app.schemas import TaskCreate, TaskOut, TaskUpdate
from app.service import TaskService

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


@app.post('/long-task')
async def start_long_task(background_tasks: BackgroundTasks):
    task_id = str(uuid4())
    background_tasks.add_task(background_tasks_.long_running_task, task_id)
    return {'task_id': task_id}


@app.get('/long-task/{task_id}/progress')
async def get_long_task_progress(task_id: str):
    progress = background_tasks_.get_progress(task_id)
    return {'progress': progress}
