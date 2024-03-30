import time
import logging
from functools import wraps

def backoff(start_sleep_time=0.1, factor=2, border_sleep_time=10, max_attempts=5):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            sleep_time = start_sleep_time
            attempts = 0
            while attempts < max_attempts:
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    logging.warning(f"Error: {e}, retrying in {sleep_time} seconds...")
                    time.sleep(sleep_time)
                    sleep_time = min(sleep_time * factor, border_sleep_time)
                    attempts += 1
            raise Exception(f"Function {func.__name__} failed after {max_attempts} attempts")
        return wrapper
    return decorator
