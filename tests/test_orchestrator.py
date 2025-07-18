import json
from pathlib import Path

from zlamida_core.agents.orchestrator_agent import OrchestratorAgent


def test_orchestrator(tmp_path: Path) -> None:
    graph = tmp_path / "graph.json"
    agent = OrchestratorAgent("orch", memory_path=graph)
    results = agent.run([
        ("echo", "a", "one"),
        ("echo", "b", "two"),
    ])
    assert results == {"a": "one", "b": "two"}
    data = json.loads(graph.read_text())
    assert len(data) == 4

