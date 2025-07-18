from __future__ import annotations

from pathlib import Path
from typing import Any, Dict, Iterable, Tuple

from .base import Agent
from zlamida_core.core.factory import AgentFactory


TaskSpec = Tuple[str, str, Any]


class OrchestratorAgent(Agent):
    """Agent that delegates tasks to other agents sequentially."""

    def __init__(self, name: str, memory_path: Path | None = None) -> None:
        super().__init__(name, memory_path)

    def run(self, tasks: Iterable[TaskSpec]) -> Dict[str, Any]:
        results: Dict[str, Any] = {}
        for agent_type, agent_name, task in tasks:
            agent = AgentFactory.create(
                agent_type, agent_name, memory_path=self.graph.path
            )
            result = agent.run(task)
            results[agent_name] = result
            self.graph.append(
                {
                    "agent": agent_name,
                    "task": task,
                    "result": result,
                    "triggered_by": self.name,
                }
            )
            self.logger.info("%s -> %s", agent_name, result)
        return results

