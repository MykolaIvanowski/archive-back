import time
from app_gateway_limit.core.redis import redis_client


class RateLimiter:
    def __init__(self, limit: int, widow_seconds: int):
        self.limit = limit
        self.widow_seconds = widow_seconds

    def is_allowed(self, key:str) -> bool:
        now = int(time.time())

        window_key = f"rate: {key} : {now // self.widow_seconds}"
        count  = redis_client.incr(window_key)

        if count == 1:
            redis_client.expire(window_key, self.widow_seconds)

        return count <= self.limit