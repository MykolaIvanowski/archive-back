import asyncio
import aiohttp
from tasks.async_task.app_fetch_10_api.http_client import get_session
from tasks.async_task.app_fetch_10_api.config import settings

# request retry + backoff
async def fetch_one(url: str):
    session = await get_session()

    for attempt in range(settings.HTTP_RETRIES + 1):
        try:
            async with session.get(url) as response:
                return await response.json()
        except aiohttp.ClientError:
            await asyncio.sleep(0.2* (attempt+1))

    return {"error": "Connection refused"}

async def fetch_parallel(url: str):
    urls =[url] * settings.PARALLEL_URLS
    tasks = [asyncio.create_task(fetch_one(url)) for url in urls]
    results = await asyncio.gather(*tasks, return_exceptions=True)
    return results