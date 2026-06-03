from fastapi import FastAPI
from app_gateway_limit.middleware.rate_limit_middleware import RateLimitMiddleware
from app_gateway_limit.middleware.rate_limit_middleware_apik_eys import ApiKeyRateLimitMiddleware

app = FastAPI()
app.add_middleware(
    RateLimitMiddleware,
    limit=100,
    window=60
)

app.add_middleware(ApiKeyRateLimitMiddleware)
