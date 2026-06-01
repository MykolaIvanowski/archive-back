from fastapi import FastAPI
from app_gateway_limit.middleware.rate_limit_middleware import RateLimitMiddleware


app = FastAPI()
app.add_middleware(
    RateLimitMiddleware,
    limit=100,
    window=60
)
