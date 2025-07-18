from pathlib import Path
import os

from zlamida_core.core.memory import ConvoGraph
from zlamida_core.core.factory import AgentFactory


def test_memory(tmp_path: Path):
    path = tmp_path / "graph.json"
    graph = ConvoGraph(path)
    graph.append({"msg": "hi"})
    assert graph.all() == [{"msg": "hi"}]
    assert path.exists()


def test_memory_creates_dirs(tmp_path: Path):
    sub = tmp_path / "sub" / "graph.json"
    graph = ConvoGraph(sub)
    graph.append({"msg": "hi"})
    assert sub.exists()


def test_agent_records(tmp_path: Path) -> None:
    path = tmp_path / "g.json"
    agent = AgentFactory.create("echo", "t", memory_path=path)
    agent.run("hello")
    graph = ConvoGraph(path)
    assert graph.all()[-1]["result"] == "hello"
