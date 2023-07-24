import os
import logging
import coloredlogs
from pythonjsonlogger import jsonlogger
from .app_mode import app_mode

_terminalfmt = "%(levelname)s - %(asctime)s - %(hostname)s - %(name)s - %(message)s"
_jsonfmt = "%(asctime)s %(hostname)s %(message)s %(name)s %(levelname)s %(module)s %(funcName)s %(filename)s %(lineno)s"
_datefmt = "%Y-%m-%d %I:%M:%S%p"

_LOG_CONSOLE = os.getenv("LOG_CONSOLE", "True")
_LOG_CONSOLE_LEVEL = os.getenv("LOG_CONSOLE_LEVEL", "DEBUG")
_LOG_CONSOLE_JSON = os.getenv("LOG_CONSOLE_JSON", "False")


def log_level(level):
    match level:
        case "INFO":
            return logging.INFO
        case "ERROR":
            return logging.ERROR
        case _:
            return logging.DEBUG


# Usage example
def setup_logger():
    # Create a custom logger
    logger = logging.getLogger(__name__)
    logger.setLevel(log_level(_LOG_CONSOLE_LEVEL))

    # Create formatter
    json_formatter = jsonlogger.JsonFormatter(
        _jsonfmt,
        json_indent=4,  # This will pretty-print your logs with an indentation of 4 spaces
        datefmt=_datefmt,
    )

    if _LOG_CONSOLE.lower() == "true":
        # Console Prints would be divided into 2 parts
        # A Colored line & A JSON with all the information

        # Colored Formatter
        coloredlogs.install(
            level="DEBUG",
            logger=logger,
            fmt=_terminalfmt,
        )

        # JSON Formatter
        if _LOG_CONSOLE_JSON.lower() == "true":
            console_handler = logging.StreamHandler()
            console_handler.setLevel(logging.DEBUG)
            console_handler.setFormatter(json_formatter)
            logger.addHandler(console_handler)

    return logger


# Use the logger
logger = setup_logger()

if app_mode.is_dev():
    # Test the logger
    logger.debug("Test Debug Message")
    logger.info("Test Info Message", extra={"more-info": "test info"})
    logger.warning("Test Warning Message")
    logger.error("Test Error Message")


__all__ = ["logger"]
