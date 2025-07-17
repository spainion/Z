from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List


class ConvoGraph:
    """Simple append-only memory graph stored in JSON."""

    def __init__(self, path: Path) -> None:
        self.path = path
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.data: List[Dict[str, Any]] = []
        if self.path.exists():
            self.data = json.loads(self.path.read_text())

    def append(self, entry: Dict[str, Any]) -> None:
        self.data.append(entry)
        self.path.write_text(json.dumps(self.data, indent=2))

    def all(self) -> List[Dict[str, Any]]:
        return list(self.data)

