"""Agent that runs shell commands."""

from __future__ import annotations

import subprocess
from typing import Any

from .base import Agent


class ShellAgent(Agent):
    """Executes shell commands and returns their output."""

    def run(self, task: Any) -> str:
        result = subprocess.run(
            task,
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
        )
        return result.stdout.strip()
