import time

from redis.commands.search.reducers import count

from app_gateway_limit.core.redis import redis_client


class AdvancedRateLimiter:
    def __init__(self, burst_limit: int, burst_refill_rate: float, sustained_limit: int,
                 sustained_window: int):
        self.burst_limit = burst_limit
        self.burst_refill_rate = burst_refill_rate
        self.sustained_limit = sustained_limit
        self.sustained_window = sustained_window


    def allowed_burst(self, key: str) -> bool:
        bucket_key = f"bucked:{key}"
        last_refill_key = f"bucked_refill:{key}"
        now = time.time()

        tokens = float(redis_client.get(bucket_key))
        last_refill  = float(redis_client.get(last_refill_key))

        tokens = float(tokens) if tokens else self.burst_limit
        last_refill = float(last_refill) if last_refill else now

        elapsed = now - last_refill
        refill  = elapsed * self.burst_refill_rate
        tokens = min(self.burst_limit, tokens + refill)

        if tokens < 1:
            return False

        tokens -= 1
        redis_client.set(bucket_key, tokens)
        redis_client.set(last_refill_key, now)
        return True

    def allowed_sustained(self, key: str) -> bool:
        now = int(time.time())
        window_key  = f"bucked_sustained: {key} : {now//self.sustained_window}"

        count = int(redis_client.get(window_key))

        if count == 1:
            redis_client.expire(window_key, self.sustained_window)

        return count <= self.sustained_limit


    def is_allowed(self, key: str) -> bool:
        return self.allowed_burst(key) and self.allowed_sustained(key)
