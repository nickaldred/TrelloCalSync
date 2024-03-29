import logging
import functools
from typing import Any, Optional
from json_log_formatter import JSONFormatter
from datetime import datetime


class CustomisedJSONFormatter(JSONFormatter):
    """Customised JSON formatter."""

    def json_record(
        self, message: str, extra: dict, record: logging.LogRecord
    ) -> dict:
        """Create a JSON log record."""
        return {
            "time_stamp": datetime.now().isoformat(),
            "log_level": record.levelname,
            **extra,
            "message": message,
        }


def get_logger() -> logging.Logger:
    """Get a logger.

    Returns:
        logging.Logger: Logger
    """

    formatter: CustomisedJSONFormatter = CustomisedJSONFormatter()

    json_handler = logging.FileHandler(
        filename="/home/nicka/projects/cal_sync/logs/cal_sync_logs.log"
    )
    json_handler.setFormatter(formatter)

    logger = logging.getLogger(__name__)
    logger.addHandler(json_handler)
    logger.setLevel(logging.INFO)
    return logger


LOGGER: logging.Logger = get_logger()


def log_decorator(func):
    """Decorator to log the start and end of a function execution."""

    @functools.wraps(func)
    def wrapper(*args, **kwargs):

        item_id: Any = kwargs.pop("item_id", None)
        LOGGER.info(
            "execution_started",
            extra={
                "item_id": item_id,
                "function_name": func.__name__,
            },
        )
        result: Any = func(*args, **kwargs)
        LOGGER.info(
            "execution_ended",
            extra={
                "item_id": item_id,
                "function_name": func.__name__,
            },
        )
        return result

    return wrapper


def debug_log_decorator(func):
    """Decorator to debug log the start and end of a function execution."""

    @functools.wraps(func)
    def wrapper(*args, **kwargs):

        item_id: Any = kwargs.pop("item_id", None)
        LOGGER.debug(
            "execution_started",
            extra={
                "item_id": item_id,
                "function_name": func.__name__,
            },
        )
        result: Any = func(*args, **kwargs)
        LOGGER.debug(
            "execution_ended",
            extra={
                "item_id": item_id,
                "function_name": func.__name__,
            },
        )
        return result

    return wrapper


def log_error(
    message: str, error_type: str, item_id: Optional[str] = None
) -> None:
    """Log an error message.

    Args:
        message (str): Error message
        error_type (str): Error type
        item_id (Optional[str], optional): Item ID. Defaults to None.

    return:
        None
    """

    LOGGER.error(
        message,
        extra={
            "item_id": item_id,
            "error_type": error_type,
            "function_name": "log_error",
        },
    )


@log_decorator
def test(item_id=None):

    try:
        result = 1 + 2
        # raise KeyError
    except KeyError as e:
        log_error("KeyError occurred", error_type="KeyError", item_id=item_id)
        raise e


test(item_id=1)
