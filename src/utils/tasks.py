import functools
import time

from core.logging import logger


def log(func, time_precision: int = 2) -> None:
    @functools.wraps(func)
    async def wrapper(*args, **kwargs) -> None:
        task_name = func.__name__.replace("_", " ")
        logger.info(f"Called task '{task_name}'")

        start_time = time.time()

        try:
            await func(*args, **kwargs)

        except Exception as e:
            logger.error(
                f"Task '{task_name}' raised an exception: {e.__repr__()}"
            )

        end_time = time.time() - start_time

        logger.info(
            f"Task '{task_name}' done,"
            f" time: {end_time:.{time_precision}f} secs"
        )

    return wrapper
