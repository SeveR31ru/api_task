import uvicorn
from fastapi import FastAPI

from api_task.database import init_db

app = FastAPI()


@app.on_event("startup")
async def on_startup():
    await init_db()


def start():
    uvicorn.run("api_task.main:app", host="0.0.0.0", port=8000, reload=True)
