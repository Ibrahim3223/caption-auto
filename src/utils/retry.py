import time
import functools
from .logger import get_logger

logger = get_logger(__name__)


def retry_with_backoff(max_retries: int = 3, base_delay: float = 1.0):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(max_retries + 1):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    if attempt == max_retries:
                        logger.error(
                            f"{func.__name__} failed after {max_retries} retries: {e}"
                        )
                        raise
                    delay = base_delay * (2 ** attempt)
                    logger.warning(
                        f"{func.__name__} attempt {attempt + 1} failed: {e}. "
                        f"Retrying in {delay}s..."
                    )
                    time.sleep(delay)
        return wrapper
    return decorator
