from __future__ import annotations

from typing import Any

import httpx

from .base import Agent


class WebAgent(Agent):
    """Agent that fetches a URL and returns its content."""

    def run(self, task: Any) -> str:
        response = httpx.get(str(task))
        response.raise_for_status()
        result = response.text
        self._record(task, result)
        return result
