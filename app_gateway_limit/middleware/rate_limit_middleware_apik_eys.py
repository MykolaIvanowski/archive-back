from fastapi import Request, HTTPException, FastAPI
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.responses import Response

from app_gateway_limit.core.rate_limiter_api_keys import ApiKeyRateLimiter


class ApiKeyRateLimitMiddleware(BaseHTTPMiddleware):
    def __init__(self, app: FastAPI) -> None:
        super().__init__(app)
        self.limiter = ApiKeyRateLimiter()


    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        api_key = request.headers.get("X-Api-Key")

        if not api_key:
            raise HTTPException(status_code=400, detail="X-Api-Key header missing")

        if not self.limiter.is_allowed(api_key):
            raise HTTPException(status_code=429, detail=f"Rate limit exceeded for api key {api_key}")

        return await call_next(request)