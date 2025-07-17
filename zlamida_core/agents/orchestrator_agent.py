from __future__ import annotations

from pathlib import Path
from typing import Any, Dict, Iterable, Tuple

from .base import Agent
from zlamida_core.core.factory import AgentFactory
from zlamida_core.core.memory import ConvoGraph
from zlamida_core.core.log import get_logger


TaskSpec = Tuple[str, str, Any]


class OrchestratorAgent(Agent):
    """Agent that delegates tasks to other agents sequentially."""

    def __init__(self, name: str, memory_path: Path | None = None) -> None:
        super().__init__(name)
        self.memory_path = memory_path or Path("convo_graph.json")
        self.graph = ConvoGraph(self.memory_path)
        self.logger = get_logger(__name__)

    def run(self, tasks: Iterable[TaskSpec]) -> Dict[str, Any]:
        results: Dict[str, Any] = {}
        for agent_type, agent_name, task in tasks:
            agent = AgentFactory.create(agent_type, agent_name)
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

