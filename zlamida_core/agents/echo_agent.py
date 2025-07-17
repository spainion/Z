from typing import Any

from .base import Agent


class EchoAgent(Agent):
    """Agent that echoes tasks."""

    def run(self, task: Any) -> Any:
        return task

