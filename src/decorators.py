import logging
import functools
import json_log_formatter
from datetime import datetime


class CustomisedJSONFormatter(json_log_formatter.JSONFormatter):
    def json_record(self, message, extra, record):
        return super(CustomisedJSONFormatter, self).json_record(
            message, extra, record
        )


formatter = CustomisedJSONFormatter()

json_handler = logging.FileHandler(
    filename="/home/nicka/projects/cal_sync/logs/cal_sync_logs.log"
)
json_handler.setFormatter(formatter)

logger = logging.getLogger(__name__)
logger.addHandler(json_handler)
logger.setLevel(logging.INFO)


def get_logger():
    return logger


def log_decorator(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        item_id = kwargs.pop("item_id", None)
        logger.info(
            "execution_started",
            extra={
                "time_stamp": datetime.now(),
                "item_id": item_id,
                "function_name": func.__name__,
            },
        )
        result = func(*args, **kwargs)
        logger.info(
            "execution_ended",
            extra={
                "time_stamp": datetime.now(),
                "item_id": item_id,
                "function_name": func.__name__,
            },
        )
        return result

    return wrapper


def debug_log_decorator(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        item_id = kwargs.pop("item_id", None)
        logger.info(
            {
                "event": "execution_started",
            },
            extra={
                "time_stamp": datetime.now(),
                "item_id": item_id,
                "function_name": func.__name__,
            },
        )
        result = func(*args, **kwargs)
        logger.info(
            {
                "event": "execution_ended",
            },
            extra={
                "time_stamp": datetime.now(),
                "item_id": item_id,
                "function_name": func.__name__,
            },
        )
        return result

    return wrapper


@log_decorator
def test():

    result = 1 + 2
    return result


print(test())
