from functools import wraps
from fastapi import HTTPException
from typing import Any
from logging import getLogger, Logger

logger: Logger = getLogger("api")

def handle_errors(default_status_code: int = 500):
    """
    Decorator that catches exceptions and converts them to HTTPException with logging.

    Args:
        default_status_code (int): HTTP status code to return if an error occurs

    Returns:
        Callable: Decorated function with error handling
    """
    def decorator(func: Any) -> (tuple[Any, ...], dict[str, Any]):
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except HTTPException:
                raise
            except Exception as e:
                logger.exception(f"Unhandled exception in {func.__name__}")
                raise HTTPException(status_code=default_status_code, detail=str(e))
        return wrapper
    return decorator
