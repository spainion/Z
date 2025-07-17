from __future__ import annotations

import abc
from typing import Any


class Agent(abc.ABC):
    """Base class for agents."""

    def __init__(self, name: str) -> None:
        self.name = name

    @abc.abstractmethod
    def run(self, task: Any) -> Any:
        """Run task and return result."""

