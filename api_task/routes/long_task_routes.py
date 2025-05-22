from fastapi import APIRouter, Depends
from sqlmodel.ext.asyncio.session import AsyncSession

from api_task import crud
from api_task.database import get_session
from api_task.models import LongTaskCreate, LongTaskRead

router = APIRouter()


@router.post("/long_tasks", response_model=LongTaskRead)
async def create_long_task(
    task: LongTaskCreate, session: AsyncSession = Depends(get_session)
):
    return await crud.create_long_task(session, task)


@router.get("/logs_tasks/", response_model=list[LongTaskRead])
async def get_long_tasks(session: AsyncSession = Depends(get_session)):
    return await crud.get_all_long_tasks(session)
