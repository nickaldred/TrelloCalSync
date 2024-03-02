import logging
import functools
import json_log_formatter
from datetime import datetime

class CustomisedJSONFormatter(json_log_formatter.JSONFormatter):
    def json_record(self, message, extra, record):
        extra['timestamp'] = datetime.now().isoformat()
        return super(CustomisedJSONFormatter, self).json_record(message, extra, record)

formatter = CustomisedJSONFormatter()

json_handler = logging.FileHandler(filename='/path/to/your/logfile.log')
json_handler.setFormatter(formatter)

logger = logging.getLogger(__name__)
logger.addHandler(json_handler)
logger.setLevel(logging.INFO)

def get_logger():
    return logger

def log_decorator(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        logger.info({'event': 'execution_started', 'name': func.__name__})
        result = func(*args, **kwargs)
        logger.info({'event': 'execution_ended', 'name': func.__name__})
        return result
    return wrapper

def debug_log_decorator(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        logger.debug({'event': 'execution_started', 'name': func.__name__})
        result = func(*args, **kwargs)
        logger.debug({'event': 'execution_ended', 'name': func.__name__})
        return result
    return wrapper

