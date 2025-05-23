import uvicorn
from fastapi import FastAPI
from fastapi.responses import RedirectResponse

import api_task.routes.long_task_routes
import api_task.routes.task_routes
from api_task.database import init_db

app = FastAPI()


app.include_router(api_task.routes.task_routes.router)
app.include_router(api_task.routes.long_task_routes.router)


@app.on_event("startup")
async def on_startup():
    await init_db()


@app.get("/", include_in_schema=False)
async def docs_redirect():
    return RedirectResponse(url="/docs")


def start():
    uvicorn.run("api_task.main:app", host="0.0.0.0", port=8000, reload=True)
