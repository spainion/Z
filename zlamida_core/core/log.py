"""Shared logging configuration."""

from __future__ import annotations

import logging
import os
from pathlib import Path

_LOG_FILE = Path(os.getenv("LOG_FILE", "zlamida.log"))
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s: %(message)s",
    handlers=[logging.FileHandler(_LOG_FILE), logging.StreamHandler()],
    force=True,
)
logging.getLogger(__name__).info("Logging to %s", _LOG_FILE)


def get_logger(name: str) -> logging.Logger:
    """Return a module-specific logger."""
    return logging.getLogger(name)
