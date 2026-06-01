from fastapi import Request, HTTPException, FastAPI
from starlette import status
from starlette.middleware.base import BaseHTTPMiddleware
from app_gateway_limit.core.rate_limiter_burst_sustained import AdvancedRateLimiter


class AdvancedRateLimitMiddleware(BaseHTTPMiddleware):
    def __init__(self, app: FastAPI) -> None:
        super().__init__(app)
        self.limiter = AdvancedRateLimiter(
            burst_limit=20,        # max tokens
            burst_refill_rate=5,   # tokens per ecc
            sustained_limit=200,   # requests
            sustained_window=60    # per minute
        )


    async def dispatch(self, request: Request, call_next):
        client_ip = request.client.host

        if not self.limiter.is_allowed(client_ip):
            raise HTTPException(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                detail="Rate limit exceeded (burst or sustained))",
            )

        return  await call_next(request)

            