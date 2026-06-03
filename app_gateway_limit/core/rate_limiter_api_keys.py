import time
import json
from app_gateway_limit.core.redis import redis_client


class ApiKeyRateLimiter:
    DEFAULT = {
        "burst": 20,
        "refill": 5,
        "sustained": 200,
        "window": 60
    }


    def get_limits(self, api_key: str):
        raw = redis_client.get(f"limits:apikey:{api_key}")
        return json.loads(raw) if raw else self.DEFAULT

    def allow_burst(self, key: str, burst: int, refill: float)-> bool:
        bucket_key = f"limits:apikey:{key}"
        refill_key = f"limits:burst:{key}"

        now = time.time()
        tokens = redis_client.get(bucket_key)
        last_refill = redis_client.get(refill_key)

        tokens = float(tokens) if tokens else burst
        last_refill = float(last_refill) if last_refill else now

        elapsed = now - last_refill
        tokens = min(burst, tokens + elapsed + refill)

        if tokens < 1:
            return False
        tokens -= 1

        redis_client.set(bucket_key, tokens)
        redis_client.set(refill_key, now)

        return True

    def allowed_sustained(self, key: str, sustained: int, window: int)-> bool:
        now = int(time.time())
        window_key = f"window:{key}:{now//window}"
        count = redis_client.get(window_key)
        if count==1:
            redis_client.expire(window_key, window)
        return count<= sustained


    def is_allowed(self, api_key: str)-> bool:
        limits = self.get_limits(api_key)
        return (self.allow_burst(api_key, limits["burst"], limits["refill"])
                and self.allowed_sustained(api_key, limits["sustained"], limits["window"]))