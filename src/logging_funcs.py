"""Functions to log messages."""

from datetime import datetime
from functools import wraps
from logging import DEBUG, INFO, FileHandler, Logger, LogRecord, getLogger
from os import environ, makedirs
from os.path import dirname
from typing import Any, Callable, Optional
from dotenv import load_dotenv
from json_log_formatter import JSONFormatter

load_dotenv("./.env")


class CustomisedJSONFormatter(JSONFormatter):
    """Customised JSON formatter."""

    def json_record(
        self, message: str, extra: dict, record: LogRecord
    ) -> dict:
        """Create a JSON log record.

        Args:
            message (str): Log message
            extra (dict): Extra information
            record (logging.LogRecord): Log record

        Returns:
            dict: JSON log record
        """

        return {
            "time_stamp": datetime.now().isoformat(),
            "log_level": record.levelname,
            **extra,
            "message": message,
        }


def get_logger(log_level: str, log_file_path: str) -> Logger:
    """Get a logger.

    Args:
        log_level (str): Log level
        log_file_path (str): Log file path

    Returns:
        logging.Logger: Logger
    """

    # Create the log file directory if it doesn't exist.
    makedirs(dirname(log_file_path), exist_ok=True)

    formatter: CustomisedJSONFormatter = CustomisedJSONFormatter()

    json_handler: FileHandler = FileHandler(
        filename=log_file_path,
    )
    json_handler.setFormatter(formatter)

    logger: Logger = getLogger(__name__)
    logger.addHandler(json_handler)

    if log_level == "DEBUG":
        logger.setLevel(DEBUG)
    else:
        logger.setLevel(INFO)

    return logger


LOGGER: Logger = get_logger(
    environ.get("LOG_LEVEL", "INFO"),
    environ.get("LOG_FILE_PATH", "tmp/logs/cal_sync_logs.log"),
)


def log_decorator(func: Callable[..., Any]) -> Callable[..., Any]:
    """Decorator to log the start and end of a function execution.

    Args:
        func (Callable[..., Any]): Function to be wrapped.

    Returns:
        Callable[..., Any]: Wrapper function.
    """

    @wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:

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


def debug_log_decorator(func: Callable[..., Any]) -> Callable[..., Any]:
    """Decorator to debug log the start and end of a function execution.

    Args:
        func (Callable[..., Any]): Function to be wrapped.

    Returns:
        Callable[..., Any]: Wrapper function.
    """

    @wraps(func)
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
    message: str,
    error_type: Optional[str] = None,
    item_id: Optional[str] = None,
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
        },
    )


def log_info(message: str, item_id: Optional[str] = None) -> None:
    """Log an info message.

    Args:
        message (str): Info message
        item_id (Optional[str], optional): Item ID. Defaults to None.

    return:
        None
    """

    LOGGER.info(
        message,
        extra={
            "item_id": item_id,
        },
    )


def log_debug(message: str, item_id: Optional[str] = None) -> None:
    """Log a debug message.

    Args:
        message (str): Debug message
        item_id (Optional[str], optional): Item ID. Defaults to None.

    return:
        None
    """

    LOGGER.debug(
        message,
        extra={
            "item_id": item_id,
        },
    )


if __name__ == "__main__":

    # Test the log_decorator function.
    @log_decorator
    def test():

        try:
            result = 1 + 2
            # raise KeyError
        except KeyError as e:
            log_error(
                "KeyError occurred", error_type="KeyError", item_id=item_id
            )
            raise e

    test(item_id=1)
