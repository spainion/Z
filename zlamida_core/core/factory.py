from __future__ import annotations

from importlib import import_module
from typing import Type

from zlamida_core.agents.base import Agent


class AgentFactory:
    """Factory to create agent instances."""

    registry: dict[str, str] = {}

    @classmethod
    def register(cls, name: str, path: str) -> None:
        cls.registry[name] = path

    @classmethod
    def create(cls, name: str, *args, **kwargs) -> Agent:
        if name not in cls.registry:
            raise ValueError(f"Agent {name} not registered")
        module_path, class_name = cls.registry[name].rsplit(".", 1)
        module = import_module(module_path)
        agent_cls: Type[Agent] = getattr(module, class_name)
        return agent_cls(*args, **kwargs)


# Register default agents
AgentFactory.register("echo", "zlamida_core.agents.echo_agent.EchoAgent")
AgentFactory.register("openai", "zlamida_core.agents.openai_agent.OpenAIAgent")

