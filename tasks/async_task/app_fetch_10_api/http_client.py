import aiohttp
from tasks.async_task.app_fetch_10_api.config import settings


async def get_session() -> aiohttp.ClientSession:
    global session
    if session is None or settings.closed:
        session = aiohttp.ClientSession(
            timeout=aiohttp.ClientTimeout(total=settings.timeout)
        )
    return session



