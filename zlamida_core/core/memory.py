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

    def refresh(self) -> None:
        """Reload data from disk if it has grown since last read."""
        if not self.path.exists():
            return
        try:
            disk_data = json.loads(self.path.read_text())
            if len(disk_data) > len(self.data):
                self.data = disk_data
                logger.info("Refreshed %d entries from %s", len(self.data), self.path)
        except json.JSONDecodeError:
            logger.warning("Corrupt memory file %s during refresh", self.path)

    def append(self, entry: Dict[str, Any]) -> None:
        self.refresh()
        self.data.append(entry)
        self.path.write_text(json.dumps(self.data, indent=2))
        logger.info("Appended entry for %s", entry.get("agent"))

    def all(self) -> List[Dict[str, Any]]:
        return list(self.data)

    def context(
        self, limit: int | None = None, agent: str | None = None
    ) -> List[Dict[str, Any]]:
        """Return recent entries, optionally filtered by agent name."""
        self.refresh()
        entries = (
            [e for e in self.data if agent is None or e.get("agent") == agent]
        )
        result = entries[-limit:] if limit else entries
        logger.info(
            "Context request agent=%s limit=%s -> %d entries",
            agent,
            limit,
            len(result),
        )
        return result

