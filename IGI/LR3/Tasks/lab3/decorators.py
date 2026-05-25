"""Reusable decorators for the lab project."""

from functools import wraps


def log_call(func):
    """Print brief start/finish messages for a called function."""

    @wraps(func)
    def wrapper(*args, **kwargs):
        print(f"\n[INFO] Running: {func.__name__}")
        result = func(*args, **kwargs)
        print(f"[INFO] Done: {func.__name__}\n")
        return result

    return wrapper
