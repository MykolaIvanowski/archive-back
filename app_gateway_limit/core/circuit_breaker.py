import time
from app_gateway_limit.core.redis import redis_client


class GlobalCircuitBreaker:

    FAILURE_THRESHOLD = 0.2
    WINDOW = 60
    OPEN_TIME = 30
    TEST_REQUESTS = 5

    def __init__(self):
        self.state_key = "cb:state"
        self.fail_key = "cb:failures"
        self.total_key = "cb:total"
        self.open_until_key = "cb:open_until"
        self.test_count_key = "cb:test_count"


    def get_state(self):
        return redis_client.get(self.state_key) or "CLOSED"

    def set_state(self, state):
        redis_client.set(self.state_key, state)


    def record_success(self):
        redis_client.incr(self.test_count_key)


    def record_failure(self):
        redis_client.incr(self.total_key)
        redis_client.incr(self.fail_key)

    def should_open(self):
        total = int(redis_client.get(self.total_key) or 0)
        fails = int(redis_client.get(self.fail_key) or 0)

        if total <= 10:
            return False

        return fails / total >= self.FAILURE_THRESHOLD

    def allowed_requests(self):
        state = self.get_state()

        if state == "OPEN":
            open_until =  float(redis_client.get(self.open_until_key) or 0)
            if time.time() < open_until:
                return False
            else:
                self.set_state("HALF-OPEN")
                redis_client.set(self.open_until_key, 0)

        if state == "HALF-OPEN":
            tests = int(redis_client.get(self.test_count_key) or 0)
            if tests >= self.TEST_REQUESTS:
                return False
            redis_client.incr(self.test_count_key)

        return True


    def update_state(self):
        if self.get_state() == "CLOSED" and self.should_open():
            self.set_state("OPEN")
            redis_client.set(self.open_until_key, time.time() + self.OPEN_TIME)

        if self.get_state() == "HALF-OPEN":
            fails = int(redis_client.get(self.fail_key) or 0)
            if fails == 0:
                self.set_state("CLOSED")
