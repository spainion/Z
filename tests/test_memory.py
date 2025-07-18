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


def test_context(tmp_path: Path) -> None:
    path = tmp_path / "g.json"
    agent_a = AgentFactory.create("echo", "a", memory_path=path)
    agent_b = AgentFactory.create("echo", "b", memory_path=path)
    agent_a.run("hi")
    agent_b.run("bye")
    graph = ConvoGraph(path)
    ctx = graph.context(limit=1, agent="a")
    assert ctx[0]["result"] == "hi"


def test_refresh(tmp_path: Path) -> None:
    path = tmp_path / "g.json"
    g1 = ConvoGraph(path)
    g2 = ConvoGraph(path)
    g1.append({"agent": "x", "task": "one", "result": "one"})
    ctx = g2.context()
    assert any(e["result"] == "one" for e in ctx)
