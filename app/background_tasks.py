import asyncio

progress_store: dict[str, int] = {}


async def long_running_task(task_id: str) -> None:
    progress_store[task_id] = 0
    while progress_store[task_id] < 100:
        await asyncio.sleep(3)
        progress_store[task_id] += 10


def get_progress(task_id: str) -> int:
    return progress_store.get(task_id, 0)
