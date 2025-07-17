from typing import Any

from .base import Agent


class EchoAgent(Agent):
    """Agent that echoes tasks and records the interaction."""

    def run(self, task: Any) -> Any:
        result = task
        self._record(task, result)
        return result

