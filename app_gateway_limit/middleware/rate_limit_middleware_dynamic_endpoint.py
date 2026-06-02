from fastapi import Request, HTTPException
from starlette.middleware.base import BaseHTTPMiddleware

from app_gateway_limit.core.rate_limiter_dynamic_endpoint import EndpointRateLimiter


class EndpointRateLimitMiddleware(BaseHTTPMiddleware):

    def __init__(self, app):
        super().__init__(app)
        self.limiter = EndpointRateLimiter()


    async def dispatch(self, request: Request, call_next):
        endpoint = request.url.path
        user =  request.headers.get("X-User-ID", "anonymous")

        if not self.limiter.is_allowed(endpoint, user):
            raise HTTPException(status_code=429,
                                detail=f"Rate limit exceeded for endpoint {endpoint}")
        return await call_next(request)