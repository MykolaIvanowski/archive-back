from fastapi import FastAPI
from tasks.async_task.app_api_fast.services.proxy_service import fetch_with_retry
from tasks.async_task.app_api_fast.config import settings


app = FastAPI()

@ app.get("/proxy")
async def get_proxy():
    data = await fetch_with_retry(settings.EXTERNAL_API_URL)
    return {"proxied": data}

@app.get("/helth")
async def helth():
    return {"status": "ok"}
