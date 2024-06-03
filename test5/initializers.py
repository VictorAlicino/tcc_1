"""Define Log for the server"""
import logging
from datetime import datetime
import colorlog

class LevelFilter(logging.Filter):
    """Log Level Filter"""
    def __init__(self, level):
        super().__init__()
        self.level = level

    def filter(self, record):
        return record.levelno >= self.level

def define_log(dirs: dict, log_level: str) -> None:
    """Logging System"""

    # Create a new log file with a timestamp in its name
    log_filename = f"{dirs['LOGS']}/opus-server-{datetime.now().strftime('%Y%m%d-%H%M%S')}.log"

    # Define the format for the log messages
    log_format = '[%(levelname)s][%(asctime)s][%(filename)s:%(lineno)d][%(name)s] %(message)s'

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

    # Create file handler
    file_handler = logging.FileHandler(log_filename, encoding='utf-8')
    file_handler.setFormatter(logging.Formatter(log_format))
    file_handler.setLevel(logging.DEBUG)

    # Create stream handler
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(color_formatter)
    stream_handler.addFilter(LevelFilter(getattr(logging, log_level.upper())))

    # Create a logger and add handlers
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)  # Capture all messages
    logger.addHandler(file_handler)
    logger.addHandler(stream_handler)

    # Set up basic configuration
    match log_level:
        case "DEBUG":
            logging.basicConfig(
                level=logging.DEBUG,
                handlers=[file_handler, stream_handler]
            )
        case "INFO":
            logging.basicConfig(
                level=logging.INFO,
                handlers=[file_handler, stream_handler]
            )
        case "WARNING":
            logging.basicConfig(
                level=logging.WARNING,
                handlers=[file_handler, stream_handler]
            )
        case "ERROR":
            logging.basicConfig(
                level=logging.ERROR,
                handlers=[file_handler, stream_handler]
            )
        case "CRITICAL":
            logging.basicConfig(
                level=logging.CRITICAL,
                handlers=[file_handler, stream_handler]
            )
        case _:
            raise ValueError("Invalid log level")
