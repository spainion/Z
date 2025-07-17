"""Shared logging configuration."""

from __future__ import annotations

import logging
from pathlib import Path

_LOG_FILE = Path("zlamida.log")
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s: %(message)s",
    handlers=[logging.FileHandler(_LOG_FILE), logging.StreamHandler()],
    force=True,
)


def get_logger(name: str) -> logging.Logger:
    """Return a module-specific logger."""
    return logging.getLogger(name)
