from fastapi import FastAPI
from tasks.async_task.app_fetch_10_api.services.parallel_fetch import fetch_parallel
from tasks.async_task.app_fetch_10_api.config import settings


app = FastAPI()

@app.get("/parallel")
async def parallel():
    results = await fetch_parallel(settings.TARGET_URL)
    return {"results": results }
