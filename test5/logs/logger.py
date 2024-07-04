import logging
from logging.config import dictConfig
from datetime import datetime
import colorlog

class LevelFilter(logging.Filter):
    """Log Level Filter"""
    def __init__(self, level):
        self.level = level

    def filter(self, record):
        return record.levelno >= self.level

def define_log(log_level: str) -> None:
    """Logging System"""

    # Create a new log file with a timestamp in its name
    log_filename = f"logs/opus-server-{datetime.now().strftime('%Y%m%d-%H%M%S')}.log"

    # Define the format for the log messages
    log_format = '[%(asctime)s] %(levelname)5s: %(message)s'

    # Define the color log format
    color_log_format = '%(log_color)s' + log_format

    # Configure the color logger
    color_formatter = colorlog.ColoredFormatter(
        color_log_format,
        datefmt='%Y-%m-%d %H:%M:%S',
        log_colors={
            'DEBUG': 'white',
            'INFO': 'cyan',
            'WARNING': 'yellow',
            'ERROR': 'red',
            'CRITICAL': 'bold_red',
        }
    )

    logging_config = {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "default": {
                "format": log_format,
                "datefmt": "%Y-%m-%d %H:%M:%S",
            },
            "color": {
                "format": color_log_format,
                "datefmt": "%Y-%m-%d %H:%M:%S",
                "()": "colorlog.ColoredFormatter",
                "log_colors": {
                    'DEBUG': 'white',
                    'INFO': 'cyan',
                    'WARNING': 'yellow',
                    'ERROR': 'red',
                    'CRITICAL': 'bold_red',
                },
            },
        },
        "handlers": {
            "file": {
                "class": "logging.FileHandler",
                "level": "DEBUG",
                "formatter": "default",
                "filename": log_filename,
                "encoding": "utf-8",
            },
            "console": {
                "class": "logging.StreamHandler",
                "level": "DEBUG",
                "formatter": "color",
                "filters": ["level_filter"],
            },
        },
        "filters": {
            "level_filter": {
                "()": LevelFilter,
                "level": getattr(logging, log_level.upper())
            }
        },
        "loggers": {
            "": {
                "handlers": ["file", "console"],
                "level": "DEBUG",
            },
            "uvicorn": {
                "handlers": ["console"],
                "level": "DEBUG",
                "propagate": False,
            },
            "uvicorn.error": {
                "handlers": ["console"],
                "level": "DEBUG",
                "propagate": False,
            },
            "uvicorn.access": {
                "handlers": ["console"],
                "level": "DEBUG",
                "propagate": False,
            },
        },
    }

    dictConfig(logging_config)
    return logging_config
