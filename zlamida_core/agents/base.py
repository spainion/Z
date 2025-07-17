from __future__ import annotations

import abc
from pathlib import Path
from typing import Any

from zlamida_core.core.memory import ConvoGraph
from zlamida_core.core.log import get_logger


class Agent(abc.ABC):
    """Base class for agents with persistent memory and logging."""

    def __init__(self, name: str, memory_path: Path | None = None) -> None:
        self.name = name
        self.graph = ConvoGraph(memory_path or Path("convo_graph.json"))
        self.logger = get_logger(self.__class__.__name__)

    @abc.abstractmethod
    def run(self, task: Any) -> Any:
        """Run task and return result."""

    def _record(self, task: Any, result: Any) -> None:
        """Persist task result and log it."""
        self.graph.append({"agent": self.name, "task": task, "result": result})
        self.logger.info("%s -> %s", self.name, result)

