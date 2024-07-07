import time


class RecursionException(Exception):
    def __init__(self, message):
        super().__init__(message)
        self.message = message

    def __str__(self):
        return self.message


def recursion_limit(interval: int = 2):
    last_call_time = 0

    def decorator(func):
        def wrapper(*args, **kwargs):
            nonlocal last_call_time
            current_time = time.time()
            if current_time - last_call_time >= interval:
                last_call_time = current_time
                return func(*args, **kwargs)
            else:
                raise RecursionException("Too much recursion")
        return wrapper
    return decorator