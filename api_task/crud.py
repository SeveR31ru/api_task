from typing import Union

from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from api_task.models import Task, TaskCreate, TaskUpdate


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
