import asyncio
import aiohttp
from tasks.async_task.app_api_fast.http_client import get_session
from tasks.async_task.app_api_fast.config import settings
from tasks.async_task.app_api_fast.utils.circuit_breaker import breaker


async def fetch_with_retry(url: str):
    if not breaker.allow():
        return {"error": "circuit_open"}
    session = await get_session()

    for attempt in range(settings.HTTP_RETRIES):
        try:
            async with session.get(url) as response:
                data = await response.json()
                breaker.record_success()
                return data
        except aiohttp.ClientError as e:
            breaker.record_failure()
            await asyncio.sleep(0.2* (attempt+1))

    return {"error": "failer_after_retries"}
