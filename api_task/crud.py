import asyncio
from datetime import datetime, timezone
from typing import Union

from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from api_task.models import LongTask, LongTaskCreate, Task, TaskCreate, TaskUpdate


async def create_task(session: AsyncSession, task_create: TaskCreate) -> Task:
    task = Task.from_orm(task_create)
    session.add(task)
    await session.commit()
    await session.refresh(task)
    return task


async def get_all_tasks(session: AsyncSession) -> list[Task]:
    result = await session.exec(select(Task))
    return result.all()


async def update_task(
    session: AsyncSession, task_id: int, task_update: TaskUpdate
) -> Union[Task, None]:
    task = await session.get(Task, task_id)
    if not task:
        return None
    task_data = task_update.dict(exclude_unset=True)
    for key, value in task_data.items():
        setattr(task, key, value)
    await session.commit()
    await session.refresh(task)
    return task


async def delete_task(session: AsyncSession, task_id: int) -> bool:
    task = await session.get(Task, task_id)
    if not task:
        return False
    await session.delete(task)
    await session.commit()
    return True


# ----дополнительное задание-----
# имитация длинной операции
async def _run_long_task(task_id: int, session: AsyncSession):
    try:
        total_steps = 120  # 2 минуты
        task = await session.get(LongTask, task_id)
        if task is None:
            raise ValueError(f"Task with id {task_id} does not exist")
        for i in range(1, total_steps + 1):
            await asyncio.sleep(1)
            task = await session.get(LongTask, task_id)
            if task:
                task.progress = int(i / total_steps * 100)
                task.updated_at = datetime.now(timezone.utc)
                await session.commit()
                task = await session.get(LongTask, task_id)

        task.status = "completed"
        task.progress = 100
        task.updated_at = datetime.now(timezone.utc)
        await session.commit()

    except Exception as e:
        if task is not None:
            task.status = "failed"
            task.updated_at = datetime.now(timezone.utc)
            await session.commit()

        raise e


async def create_long_task(session: AsyncSession, task_create: LongTaskCreate) -> Task:
    task = LongTask.from_orm(task_create)
    session.add(task)
    await session.commit()
    await session.refresh(task)
    asyncio.create_task(_run_long_task(task.id, session))
    return task


async def get_all_long_tasks(session: AsyncSession) -> list[Task]:
    result = await session.exec(select(LongTask))
    return result.all()
