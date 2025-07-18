"""Run agents in separate processes."""

from __future__ import annotations

from concurrent.futures import ProcessPoolExecutor, as_completed
from typing import Any, Dict, Iterable, Tuple

from .factory import AgentFactory

TaskSpec = Tuple[str, str, Any]


def _run_agent(agent_type: str, name: str, task: Any) -> tuple[str, Any]:
    agent = AgentFactory.create(agent_type, name)
    return name, agent.run(task)


def run_agents(
    tasks: Iterable[TaskSpec], max_workers: int | None = None
) -> Dict[str, Any]:
    """Execute agents concurrently using processes."""
    results: Dict[str, Any] = {}
    with ProcessPoolExecutor(max_workers=max_workers) as executor:
        future_to_name = {
            executor.submit(_run_agent, agent_type, name, task): name
            for agent_type, name, task in tasks
        }
        for future in as_completed(future_to_name):
            name, result = future.result()
            results[name] = result
    return results
