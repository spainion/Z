from __future__ import annotations

from typing import Any

import os
import httpx

from pathlib import Path

from .base import Agent


class WebAgent(Agent):
    """Agent that fetches a URL and returns its content."""

    DEFAULT_TIMEOUT: float = 10.0
    DEFAULT_USER_AGENT: str = "ZLAMIDA-Core WebAgent"
    USER_AGENT: str = DEFAULT_USER_AGENT

    def __init__(
        self,
        name: str,
        memory_path: Path | None = None,
        *,
        timeout: float | None = None,
        user_agent: str | None = None,
    ) -> None:
        super().__init__(name, memory_path)
        self.timeout = timeout or float(os.getenv("WEB_AGENT_TIMEOUT", str(self.DEFAULT_TIMEOUT)))
        self.user_agent = user_agent or os.getenv("WEB_AGENT_UA", self.DEFAULT_USER_AGENT)

    def run(self, task: Any) -> str:
        """Retrieve the URL specified by ``task`` and record the result."""
        response = httpx.get(
            str(task),
            headers={"User-Agent": self.user_agent},
            timeout=self.timeout,
        )
        response.raise_for_status()
        result = response.text
        self._record(task, result)
        return result
