import aiohttp
from tasks.async_task.app_api_fast.config import settings

session: aiohttp.ClientSession | None = None

async def get_session() -> aiohttp.ClientSession:
    global session
    if session is None or session.closed:
        session = aiohttp.ClientSession(
            timeout=aiohttp.ClientTimeout(total=settings.TIMEOUT)
        )
    return session

