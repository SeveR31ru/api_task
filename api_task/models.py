from datetime import datetime
from typing import Optional

from sqlmodel import Field, SQLModel


class TaskBase(SQLModel):
    title: str
    description: Optional[str] = None
    completed: bool = False


class Task(TaskBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)


class TaskCreate(TaskBase):
    pass


class TaskRead(TaskBase):
    id: int


class TaskUpdate(SQLModel):
    title: Optional[str] = None
    description: Optional[str] = None
    completed: Optional[bool] = None


# ---------Дополнительное задание-----------


class LongTaskBase(SQLModel):
    status: str = "in progress"
    progress: int = 0
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)


class LongTask(LongTaskBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)


class LongTaskRead(LongTaskBase):
    id: int


class LongTaskCreate(LongTaskBase):
    pass
