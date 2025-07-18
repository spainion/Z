from __future__ import annotations

"""Agent that uses OpenAI's async API."""

import asyncio
import os
from pathlib import Path
from typing import Any

import openai

from .base import Agent


class AsyncOpenAIAgent(Agent):
    """Agent that performs chat completion asynchronously."""

    def __init__(self, name: str, model: str = "gpt-4o-mini", memory_path: Path | None = None) -> None:
        super().__init__(name, memory_path)
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise RuntimeError("OPENAI_API_KEY not set")
        self.client = openai.AsyncOpenAI(api_key=api_key)
        self.model = model

    async def arun(self, task: Any) -> str:
        completion = await self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": str(task)}],
            temperature=0.7,
        )
        result = completion.choices[0].message.content.strip()
        self._record(task, result)
        return result

    def run(self, task: Any) -> str:
        return asyncio.run(self.arun(task))

