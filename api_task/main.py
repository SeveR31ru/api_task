import uvicorn
from fastapi import FastAPI

import api_task
import api_task.routes
import api_task.routes.task_routes
from api_task.database import init_db

app = FastAPI()

app.include_router(api_task.routes.task_routes.router)


@app.on_event("startup")
async def on_startup():
    await init_db()


def start():
    uvicorn.run("api_task.main:app", host="0.0.0.0", port=8000, reload=True)
