import json
from pathlib import Path

from zlamida_core.agents.parallel_orchestrator_agent import ParallelOrchestratorAgent


def test_parallel_orchestrator(tmp_path: Path) -> None:
    graph = tmp_path / "graph.json"
    agent = ParallelOrchestratorAgent("orch", memory_path=graph)
    results = agent.run([
        ("echo", "a", "one"),
        ("echo", "b", "two"),
    ])
    assert results == {"a": "one", "b": "two"}
    data = json.loads(graph.read_text())
    assert len(data) == 2


def test_parallel_orchestrator_limit_workers(tmp_path: Path) -> None:
    graph = tmp_path / "graph.json"
    agent = ParallelOrchestratorAgent("orch", max_workers=1, memory_path=graph)
    results = agent.run([
        ("echo", "a", "one"),
        ("echo", "b", "two"),
    ])
    assert results == {"a": "one", "b": "two"}

