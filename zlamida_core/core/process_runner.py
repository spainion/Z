"""Run agents in separate processes."""

from __future__ import annotations

from multiprocessing import Process, Queue
from typing import Any, Dict, Iterable, Tuple

from .factory import AgentFactory

TaskSpec = Tuple[str, str, Any]


def _run_agent(q: Queue, agent_type: str, name: str, task: Any) -> None:
    agent = AgentFactory.create(agent_type, name)
    q.put((name, agent.run(task)))


def run_agents(tasks: Iterable[TaskSpec]) -> Dict[str, Any]:
    """Execute agents concurrently using processes."""
    q: Queue = Queue()
    procs = [
        Process(target=_run_agent, args=(q, agent_type, name, task))
        for agent_type, name, task in tasks
    ]
    for p in procs:
        p.start()
    results: Dict[str, Any] = {}
    for _ in procs:
        name, result = q.get()
        results[name] = result
    for p in procs:
        p.join()
    return results
