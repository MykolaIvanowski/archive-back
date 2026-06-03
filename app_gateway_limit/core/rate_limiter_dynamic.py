import time
import json
from app_gateway_limit.core.redis import redis_client


class DynamicRateLimiter:
    DEFAULT_BURST_LIMIT = 20
    DEFAULT_REFILL = 5
    DEFAULT_SUSTAINED = 200
    DEFAULT_WINDOW = 60

    def get_limits(self, user_key: str):
        raw = redis_client.get(f"limits:{user_key}")
        if not raw:
            return {
                "burst": self.DEFAULT_BURST_LIMIT,
                "refill": self.DEFAULT_REFILL,
                "sustained": self.DEFAULT_SUSTAINED,
                "window": self.DEFAULT_WINDOW,
            }
        return json.loads(raw)


    def allow_burst(self, key: str, burst: int, refill: float ) -> bool:
        burst_key = f"bucket:{key}"
        refill_key = f"bucket_refill:{key}"
        now = time.time()

        tokens = redis_client.get(burst_key)
        last_refill = redis_client.get(refill_key)

        tokens = float(tokens) if tokens else burst
        last_refill = float(last_refill) if last_refill else now

        elapsed = now - last_refill
        tokens = min(burst, tokens + elapsed + refill)

        if tokens < 1:
            return False

        tokens -= 1
        redis_client.set(burst_key, tokens)
        redis_client.set(refill_key, now)

        return True


    def allow_sustained(self, key: int, sustained: int, window: int ) -> bool:
        now = time.time()
        window_key = f"window:{key}:{now//window}"
        count = redis_client.incr(window_key)
        if count == 1:
            redis_client.expire(window_key, window)

        return count <= sustained

    def is_allowed(self, user_key: str) -> bool:
        limits = self.get_limits(user_key)

        return (
            self.allow_burst(user_key, limits["burst"], limits["refill"])
            and self.allow_sustained(user_key, limits["sustained"], limits["window"])
        )