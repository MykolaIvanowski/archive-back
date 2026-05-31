from fastapi import Request, HTTPException, FastAPI
from starlette import status
from starlette.middleware.base import BaseHTTPMiddleware

from app_gateway_limit.core.rate_limiter import RateLimiter


class RateLimitMiddleware(BaseHTTPMiddleware):
    def __init__(self, app: FastAPI, limit: int, window: int) -> None:
        super().__init__(app)
        self.limit = RateLimiter(limit, window)

    async def dispatch(self, request: Request, call_next):
        client_ip  = request.client.host

        if not self.limit.is_allowed(client_ip):
            raise HTTPException(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                detail="Too many requests",
            )
        return await call_next(request)