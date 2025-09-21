"""Logging utility."""

import logging
import sys


def get_logger(name: str) -> logging.Logger:
    """Return a logger for the given file/module name."""
    logger = logging.getLogger(name=name)

    if not logger.handlers:  # avoid duplicate handlers
        logger.setLevel(level=logging.DEBUG)

        handler: logging.StreamHandler[logging.TextIO | logging.Any] = (
            logging.StreamHandler(stream=sys.stdout)
        )
        handler.setLevel(level=logging.DEBUG)

        fmt = logging.Formatter(
            fmt="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )
        handler.setFormatter(fmt=fmt)

        logger.addHandler(hdlr=handler)

    return logger
