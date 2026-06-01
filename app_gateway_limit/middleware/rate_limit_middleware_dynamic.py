from fastapi import Request, HTTPException, FastAPI
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.responses import Response

from app_gateway_limit.core.rate_limiter_dynamic import DynamicRateLimiter


class DynamicRateLimitMiddleware(BaseHTTPMiddleware):

    def __init__(self, app: FastAPI) -> None:
        super().__init__(app)
        self.limiter = DynamicRateLimiter()


    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        user = request.headers.get("x-user-key")

        if user is None:
            raise HTTPException(status_code=400, detail="x-user-key header missing")

        if not self.limiter.is_allowed(user):
            raise HTTPException(status_code=429, detail="Rate limit exceeded for user")

        return await call_next(request)