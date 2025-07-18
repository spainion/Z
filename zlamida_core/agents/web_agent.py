from __future__ import annotations

from typing import Any

import httpx

from .base import Agent


class WebAgent(Agent):
    """Agent that fetches a URL and returns its content."""

    DEFAULT_TIMEOUT: float = 10.0
    USER_AGENT: str = "ZLAMIDA-Core WebAgent"

    def run(self, task: Any) -> str:
        """Retrieve the URL specified by ``task`` and record the result."""
        response = httpx.get(
            str(task),
            headers={"User-Agent": self.USER_AGENT},
            timeout=self.DEFAULT_TIMEOUT,
        )
        response.raise_for_status()
        result = response.text
        self._record(task, result)
        return result
