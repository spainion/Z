from __future__ import annotations

"""Agent that runs tasks concurrently using other agents."""

from pathlib import Path
from typing import Any, Dict, Iterable, Tuple

from .base import Agent
from zlamida_core.core import runner, process_runner
from zlamida_core.core.factory import AgentFactory

TaskSpec = Tuple[str, str, Any]


class ParallelOrchestratorAgent(Agent):
    """Run delegated tasks in parallel using threads or processes."""

    def __init__(self, name: str, use_process: bool = False, memory_path: Path | None = None) -> None:
        super().__init__(name, memory_path)
        self.use_process = use_process

    def run(self, tasks: Iterable[TaskSpec]) -> Dict[str, Any]:
        run_fn = process_runner.run_agents if self.use_process else runner.run_agents
        task_list = list(tasks)
        results = run_fn([(a, n, t) for a, n, t in task_list])
        for agent_type, agent_name, task in task_list:
            self.graph.append({
                "agent": agent_name,
                "task": task,
                "result": results[agent_name],
                "triggered_by": self.name,
            })
            self.logger.info("%s -> %s", agent_name, results[agent_name])
        return results

