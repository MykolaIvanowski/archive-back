import time
import json
import token

from app_gateway_limit.core.redis import redis_client


class EndpointRateLimiter:
    DEFAULT = {
        "burst": 20,
        "refill": 5,
        "sustained": 200,
        "window": 60
    }

    def get_limits(self, endpoints: str):
        raw = redis_client.get(f"limits:endpoint:{endpoints}")
        return json.loads(raw) if raw else self.DEFAULT


    def allowed_burst(self, key: str,  burst: int, refill: float)-> bool:
        bucket_key =  f"bucket:{key}"
        refill_key = f"bucket_refill:{key}"

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
        window_key = f"window:{key}:{now // window}"

        count = redis_client.get(window_key)
        if count==1:
            redis_client.expire(window_key, window)

        return count <= sustained

    def is_allowed(self, endpoint: str, user_key: str)-> bool:
        limits = self.get_limits(endpoint)
        composed_key = f"{endpoint}:{user_key}"

        return (
            self.allowed_burst(composed_key, limits["burst"], limits["refill"])
            and self.allowed_sustained(composed_key, limits["sustained"], limits["window"])
        )