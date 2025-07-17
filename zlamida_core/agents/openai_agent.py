"""Agent that delegates tasks to OpenAI's chat completion API."""

from __future__ import annotations

import os
from typing import Any

import openai

from .base import Agent


class OpenAIAgent(Agent):
    """Agent using OpenAI's API to generate responses."""

    def __init__(self, name: str, model: str = "gpt-4o-mini") -> None:
        super().__init__(name)
        self.model = model
        self.api_key = os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise RuntimeError("OPENAI_API_KEY not set")
        openai.api_key = self.api_key

    def run(self, task: Any) -> str:
        completion = openai.ChatCompletion.create(
            model=self.model,
            messages=[{"role": "user", "content": str(task)}],
            temperature=0.7,
        )
        return completion.choices[0].message["content"].strip()

