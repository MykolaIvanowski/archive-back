import time

class CircuitBreaker:
    def __init__(self, fail_threshold: int, reset_timeout: int):
        self.fail_threshold = fail_threshold
        self.reset_timeout = reset_timeout
        self.fail_count = 0
        self.open_until = 0


    def allow(self)->bool:
        return  time.time() >= self.open_until


    def record_success(self):
        self.fail_count = 0

    def record_failure(self):
        self.fail_count += 1
        if self.fail_count >= self.fail_threshold:
            self.open_until = time.time() + self.reset_timeout

breaker = CircuitBreaker(
    fail_threshold=5,
    reset_timeout=30
)