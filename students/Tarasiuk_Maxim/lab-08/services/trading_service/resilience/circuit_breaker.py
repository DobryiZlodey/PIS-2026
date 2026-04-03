import time
from functools import wraps

class CircuitBreakerOpenException(Exception):
    pass

class CircuitBreaker:
    def __init__(self, exceptions=(Exception,), failure_threshold=3, recovery_time=5):
        self.exceptions = exceptions
        self.failure_threshold = failure_threshold
        self.recovery_time = recovery_time
        
        self.failure_count = 0
        self.last_failure_time = None
        self.state = "CLOSED" # CLOSED, OPEN, HALF-OPEN

    def call(self, func, *args, **kwargs):
        if self.state == "OPEN":
            if time.time() - self.last_failure_time > self.recovery_time:
                self.state = "HALF-OPEN"
            else:
                raise CircuitBreakerOpenException("Circuit is OPEN. Fast failing.")
                
        try:
            result = func(*args, **kwargs)
            if self.state == "HALF-OPEN":
                self.reset()
            return result
        except self.exceptions as e:
            self.failure_count += 1
            if self.failure_count >= self.failure_threshold:
                self.state = "OPEN"
                self.last_failure_time = time.time()
            raise e
            
    def reset(self):
        self.failure_count = 0
        self.state = "CLOSED"
        self.last_failure_time = None

def circuit_breaker(failure_threshold=3, recovery_time=5):
    breaker = CircuitBreaker(failure_threshold=failure_threshold, recovery_time=recovery_time)
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            return breaker.call(func, *args, **kwargs)
        return wrapper
    return decorator
