"""Agent that delegates tasks to OpenAI's chat completion API."""

from __future__ import annotations

import os
from pathlib import Path
from typing import Any

import openai

from .base import Agent


class OpenAIAgent(Agent):
    """Agent using OpenAI's API to generate responses."""

    def __init__(self, name: str, model: str = "gpt-4o-mini", memory_path: Path | None = None) -> None:
        super().__init__(name, memory_path)
        self.model = model
        self.api_key = os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise RuntimeError("OPENAI_API_KEY not set")
        openai.api_key = self.api_key

    def run(self, task: Any) -> str:
        completion = openai.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": str(task)}],
            temperature=0.7,
        )
        result = completion.choices[0].message.content.strip()
        self._record(task, result)
        return result

