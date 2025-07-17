from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List

from .log import get_logger


logger = get_logger(__name__)


class ConvoGraph:
    """Simple append-only memory graph stored in JSON."""

    def __init__(self, path: Path) -> None:
        self.path = path
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.data: List[Dict[str, Any]] = []
        if self.path.exists():
            try:
                self.data = json.loads(self.path.read_text())
                logger.info("Loaded %d entries from %s", len(self.data), self.path)
            except json.JSONDecodeError:
                logger.warning("Corrupt memory file %s, starting fresh", self.path)
                self.data = []

    def append(self, entry: Dict[str, Any]) -> None:
        self.data.append(entry)
        self.path.write_text(json.dumps(self.data, indent=2))
        logger.info("Appended entry for %s", entry.get("agent"))

    def all(self) -> List[Dict[str, Any]]:
        return list(self.data)

