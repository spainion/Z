"""Utilities for running multiple agents concurrently."""

from __future__ import annotations

from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Any, Dict, Iterable, Tuple

from .factory import AgentFactory


TaskSpec = Tuple[str, str, Any]


def run_agents(tasks: Iterable[TaskSpec]) -> Dict[str, Any]:
    """Run multiple agents in parallel.

    Args:
        tasks: Iterable of (agent_type, name, task) tuples.

    Returns:
        Mapping of agent names to their results.
    """
    results: Dict[str, Any] = {}
    with ThreadPoolExecutor() as executor:
        future_to_name = {
            executor.submit(
                AgentFactory.create(agent_type, name).run, task
            ): name
            for agent_type, name, task in tasks
        }
        for future in as_completed(future_to_name):
            name = future_to_name[future]
            results[name] = future.result()
    return results
