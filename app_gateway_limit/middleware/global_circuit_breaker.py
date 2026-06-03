from fastapi import Request, HTTPException, FastAPI
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.responses import Response

from app_gateway_limit.core.circuit_breaker import GlobalCircuitBreaker


class CircuitBreakerMiddleware(BaseHTTPMiddleware):

    def __init__(self, app: FastAPI) -> None:
        super().__init__(app)
        self.circuit_breaker = GlobalCircuitBreaker()


    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        if not self.circuit_breaker.allowed_requests():
            raise HTTPException(status_code=503, detail="Server temporarily overloaded")
        try:
            response = await call_next(request)
            self.circuit_breaker.record_success()
        except Exception:
            self.circuit_breaker.record_failure()
            self.circuit_breaker.update_state()
            raise

        self.circuit_breaker.update_state()
        return response