import logging

import colorlog as colorlog

__all__ = [
    "init_logging",
    "get_logger",
    "LOG_FORMAT_DEBUG",
    "LOG_FORMAT_CONCISE",
]


LOG_LEVEL = logging.DEBUG
LOG_FORMAT_DEBUG = "[%(asctime)s %s(levelname)] (%(name)s:%(lineno)s) %(message)s"
LOG_FORMAT_CONCISE = "%(message)s"
LOG_FORMAT = LOG_FORMAT_CONCISE


root_logger = logging.getLogger()


def init_root_logger(level, fmt):
    colored_formatter = colorlog.ColoredFormatter(
        '%(log_color)s' + fmt,
        log_colors={
            "DEBUG": "white",
            "INFO": "blue",
            "WARNING": "yellow",
            "ERROR": "red",
            "CRITICAL": "bold_red",
        }
    )
    stdio_handler = colorlog.StreamHandler()
    stdio_handler.setFormatter(colored_formatter)
    root_logger.addHandler(stdio_handler)
    root_logger.setLevel(level)


def init_logging(level=LOG_LEVEL, fmt=LOG_FORMAT, force=False):
    if (not force) and root_logger.handlers:
        return
    init_root_logger(level, fmt)


def get_logger(name, level=None):
    logger = logging.getLogger(name)
    if level is not None:
        logger.setLevel(level)
    return logger


logger = get_logger("storygen.log")


def main():
    init_logging()
    logger.debug("Logging initialized")
    logger.info("Logging initialized")
    logger.warning("Logging initialized")
    logger.error("Logging initialized")
    logger.critical("Logging initialized")


if __name__ == '__main__':
    main()
