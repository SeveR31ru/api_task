from fastapi import APIRouter, Depends, HTTPException
from sqlmodel.ext.asyncio.session import AsyncSession

from api_task import crud
from api_task.database import get_session
from api_task.models import TaskCreate, TaskRead, TaskUpdate

router = APIRouter()


@router.post("/tasks/", response_model=TaskRead)
async def create_task(task: TaskCreate, session: AsyncSession = Depends(get_session)):
    return await crud.create_task(session, task)


@router.get("/tasks/", response_model=list[TaskRead])
async def get_tasks(session: AsyncSession = Depends(get_session)):
    return await crud.get_all_tasks(session)


@router.put("/tasks/{task_id}", response_model=TaskRead)
async def update_task(
    task_id: int, task: TaskUpdate, session: AsyncSession = Depends(get_session)
):
    result = await crud.update_task(session, task_id, task)
    if not result:
        raise HTTPException(status_code=404, detail="Task not found")
    return result


@router.delete("/tasks/{task_id}")
async def delete_task(task_id: int, session: AsyncSession = Depends(get_session)):
    result = await crud.delete_task(session, task_id)
    if not result:
        raise HTTPException(status_code=404, detail="Task not found")
    return {"ok": True}
